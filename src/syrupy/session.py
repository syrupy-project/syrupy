from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)
from enum import Enum
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Optional,
)

import pytest

from .constants import EXIT_STATUS_FAIL_UNUSED
from .data import SnapshotCollections
from .exceptions import FailedToLoadModuleMember
from .location import PyTestLocation
from .report import SnapshotReport
from .types import (
    SerializedData,
    SnapshotIndex,
)
from .utils import (
    cleanup_snapshot_write_sidecars,
    compress_json,
    decompress_json,
    import_module_member,
    is_xdist_gw0,
    is_xdist_worker,
    set_snapshot_file_lock,
    should_use_snapshot_file_lock,
    warn_selected_collected_mismatch,
)

# Snapshot collections on the report that are merged across pytest-xdist workers.
_MERGED_COLLECTIONS = ("discovered", "created", "failed", "matched", "updated", "used")


class _ReconstructedObject:
    """Stand-in for ``item.obj`` rebuilt from a worker's serialized item."""

    def __init__(self, modulename: str, methodname: str) -> None:
        self.__module__ = modulename
        self.__name__ = methodname


class _ReconstructedItem:
    """
    Stand-in for a ``pytest.Item`` rebuilt from a worker's serialized payload.

    Normally the xdist controller already has real collected items; worker
    ``collected`` data is applied only when the controller's set is empty.
    Reconstruction supplies enough of the pytest item for
    ``PyTestLocation`` to resolve snapshot names and locations.
    """

    def __init__(self, data: dict[str, str]) -> None:
        self.nodeid = data["nodeid"]
        self.name = data["name"]
        self.path = Path(data["path"])
        self.obj = _ReconstructedObject(data["modulename"], data["methodname"])


if TYPE_CHECKING:
    from .assertion import SnapshotAssertion
    from .extensions.base import AbstractSyrupyExtension


class ItemStatus(Enum):
    NOT_RUN = False
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


_QueuedWriteExtensionKey = tuple[type["AbstractSyrupyExtension"], str]
_QueuedWriteTestLocationKey = tuple["PyTestLocation", "SnapshotIndex"]


@dataclass
class SnapshotSession:
    pytest_session: "pytest.Session"

    # List of file extensions to ignore during discovery/processing
    ignore_file_extensions: list[str] | None = None

    # Snapshot report generated on finish
    report: Optional["SnapshotReport"] = None
    # All the collected test items, keyed by nodeid to preserve collection order
    _collected_items: dict[str, "pytest.Item"] = field(default_factory=dict)
    # All the selected test items. Will be set to False until the test item is run.
    _selected_items: dict[str, ItemStatus] = field(default_factory=dict)
    _assertions: list["SnapshotAssertion"] = field(default_factory=list)
    _extensions: dict[str, "AbstractSyrupyExtension"] = field(default_factory=dict)
    # Reports published by pytest-xdist workers, collected on the controller.
    _worker_reports: list[dict[str, Any]] = field(default_factory=list)

    _locations_discovered: defaultdict[str, set[Any]] = field(
        default_factory=lambda: defaultdict(set)
    )

    # For performance, we buffer snapshot writes in memory before flushing them to disk. In
    # particular, we want to be able to write to a file on disk only once, rather than having to
    # repeatedly rewrite it.
    #
    # That batching leads to using two layers of dicts here: the outer layer represents the
    # extension/file-location pair that will be written, and the inner layer represents the
    # snapshots within that, "indexed" to allow efficient recall.
    _queued_snapshot_writes: defaultdict[
        _QueuedWriteExtensionKey,
        dict[_QueuedWriteTestLocationKey, "SerializedData"],
    ] = field(default_factory=lambda: defaultdict(dict))

    # Snapshot files written this session (for lock/tmp sidecar cleanup).
    _written_snapshot_locations: set[str] = field(default_factory=set)

    def _snapshot_write_queue_keys(
        self,
        extension: "AbstractSyrupyExtension",
        test_location: "PyTestLocation",
        index: "SnapshotIndex",
    ) -> tuple[_QueuedWriteExtensionKey, _QueuedWriteTestLocationKey]:
        snapshot_location = extension.get_location(
            test_location=test_location, index=index
        )
        return (extension.__class__, snapshot_location), (test_location, index)

    def queue_snapshot_write(
        self,
        extension: "AbstractSyrupyExtension",
        test_location: "PyTestLocation",
        data: "SerializedData",
        index: "SnapshotIndex",
    ) -> None:
        ext_key, loc_key = self._snapshot_write_queue_keys(
            extension, test_location, index
        )
        self._queued_snapshot_writes[ext_key][loc_key] = data
        if extension.write_immediately:
            self._flush_snapshot_write_queue_key(ext_key)

    def _flush_snapshot_write_queue_key(
        self, ext_key: _QueuedWriteExtensionKey
    ) -> None:
        queued_write = self._queued_snapshot_writes.pop(ext_key, None)
        if not queued_write:
            return
        extension_class, snapshot_location = ext_key
        name_order = (
            self.snapshot_name_order() if self.snapshot_declaration_order else None
        )
        # Track before write so lock/tmp sidecars are cleaned even if acquire
        # times out after creating the lock file.
        if self.snapshot_file_lock:
            self._written_snapshot_locations.add(snapshot_location)
        extension_class.write_snapshot(
            snapshot_location=snapshot_location,
            snapshots=[
                (data, loc, index) for (loc, index), data in queued_write.items()
            ],
            name_order=name_order,
        )

    def flush_snapshot_write_queue(self) -> None:
        for ext_key in list(self._queued_snapshot_writes):
            self._flush_snapshot_write_queue_key(ext_key)

    def recall_snapshot(
        self,
        extension: "AbstractSyrupyExtension",
        test_location: "PyTestLocation",
        index: "SnapshotIndex",
    ) -> Optional["SerializedData"]:
        """Find the current value of the snapshot, for this session, either a pending write or the actual snapshot."""

        ext_key, loc_key = self._snapshot_write_queue_keys(
            extension, test_location, index
        )
        data = self._queued_snapshot_writes[ext_key].get(loc_key)
        if data is not None:
            return data

        # No matching write queued, so just read the snapshot directly:
        return extension.read_snapshot(
            test_location=test_location, index=index, session_id=str(id(self))
        )

    @property
    def update_snapshots(self) -> bool:
        return bool(self.pytest_session.config.option.update_snapshots)

    @property
    def warn_unused_snapshots(self) -> bool:
        return bool(self.pytest_session.config.option.warn_unused_snapshots)

    @property
    def disable_unused_snapshots(self) -> bool:
        return bool(
            getattr(
                self.pytest_session.config.option, "disable_unused_snapshots", False
            )
        )

    @property
    def snapshot_declaration_order(self) -> bool:
        return bool(
            getattr(
                self.pytest_session.config.option, "snapshot_declaration_order", False
            )
        )

    @property
    def snapshot_file_lock(self) -> bool:
        """True under pytest-xdist so concurrent amber writes do not clobber."""
        return should_use_snapshot_file_lock(self.pytest_session.config)

    @property
    def snapshot_file_lock_timeout(self) -> float:
        return float(
            getattr(
                self.pytest_session.config.option,
                "snapshot_file_lock_timeout",
                60.0,
            )
        )

    def snapshot_name_order(self) -> dict[str, int]:
        """Map snapshot names to pytest collection index (declaration order)."""
        order: dict[str, int] = {}
        for index, item in enumerate(self._collected_items.values()):
            name = PyTestLocation(item).snapshot_name
            if name not in order:
                order[name] = index
        return order

    def collect_items(self, items: list["pytest.Item"]) -> None:
        for item in self.filter_valid_items(items):
            self._collected_items[item.nodeid] = item

    def select_items(self, items: list["pytest.Item"]) -> None:
        for item in self.filter_valid_items(items):
            self._selected_items[getattr(item, "nodeid")] = (  # noqa: B009
                ItemStatus.NOT_RUN
            )

    def start(self) -> None:
        self.report = None
        self._collected_items = {}
        self._selected_items = {}
        self._assertions = []
        self._extensions = {}
        self._locations_discovered = defaultdict(set)
        self._written_snapshot_locations = set()
        self._worker_reports = []
        # Mirror config.option into the context used by amber write/delete.
        set_snapshot_file_lock(
            self.snapshot_file_lock, timeout=self.snapshot_file_lock_timeout
        )

    def ran_item(
        self, nodeid: str, outcome: Literal["passed", "skipped", "failed"]
    ) -> None:
        if nodeid in self._selected_items:
            try:
                self._selected_items[nodeid] = ItemStatus(outcome)
            except ValueError:
                pass  # if we don't understand the outcome, leave the item as "not run"

    @staticmethod
    def _serialize_item(item: "pytest.Item") -> dict[str, str]:
        obj = item.obj  # type: ignore[attr-defined]
        return {
            "nodeid": item.nodeid,
            "name": item.name,
            "path": str(item.path),
            "modulename": obj.__module__,
            "methodname": obj.__name__,
        }

    def _publish_write_sidecars(self) -> None:
        """Tell the controller which snapshot files this worker wrote."""
        output = getattr(self.pytest_session.config, "workeroutput", None)
        if output is None:
            return
        output["syrupy_write_sidecars"] = sorted(self._written_snapshot_locations)

    def _publish_worker_report(self) -> None:
        """Stash this worker's report on ``config.workeroutput`` for the controller."""
        output = getattr(self.pytest_session.config, "workeroutput", None)
        if output is None or self.report is None:
            return
        collections = {
            name: getattr(self.report, name).serialize() for name in _MERGED_COLLECTIONS
        }
        payload: dict[str, Any] = {
            "collections": compress_json(collections),
            "num_xfails": self.report._num_xfails,
            "selected": {
                nodeid: status.value for nodeid, status in self._selected_items.items()
            },
            "extensions": {
                location: (
                    f"{extension.__class__.__module__}"
                    f".{extension.__class__.__qualname__}"
                )
                for location, extension in self._extensions.items()
            },
        }
        # Every worker collects the identical full set; only gw0 sends it.
        # Compress to shrink the xdist workeroutput IPC payload on large suites.
        if is_xdist_gw0():
            payload["collected"] = compress_json(
                [self._serialize_item(item) for item in self._collected_items.values()]
            )
        output["syrupy_report"] = payload

    def add_worker_report(self, report: dict[str, Any]) -> None:
        """Called on the controller for each worker as it shuts down."""
        self._worker_reports.append(report)

    def add_written_snapshot_locations(self, locations: list[str]) -> None:
        """Record snapshot files written by a worker (for sidecar cleanup)."""
        self._written_snapshot_locations.update(locations)

    def _cleanup_write_sidecars(self) -> None:
        cleanup_snapshot_write_sidecars(*self._written_snapshot_locations)
        self._written_snapshot_locations.clear()

    def _merge_worker_reports(self) -> None:
        assert self.report is not None
        selected: dict[str, ItemStatus] = {}
        for report in self._worker_reports:
            self.report._num_xfails += report["num_xfails"]
            serialized_collections = report["collections"]
            if isinstance(serialized_collections, bytes):
                serialized_collections = decompress_json(serialized_collections)
            for name, serialized in serialized_collections.items():
                getattr(self.report, name).merge_serialized(serialized)
            for nodeid, value in report["selected"].items():
                status = ItemStatus(value)
                # Prefer a concrete run status over NOT_RUN from another worker.
                if selected.get(nodeid, ItemStatus.NOT_RUN) == ItemStatus.NOT_RUN:
                    selected[nodeid] = status
            for location, member in report.get("extensions", {}).items():
                if location not in self._extensions:
                    try:
                        self._extensions[location] = import_module_member(member)()
                    except FailedToLoadModuleMember:
                        pass
            if "collected" in report and not self.report.collected_items:
                collected = report["collected"]
                if isinstance(collected, bytes):
                    collected = decompress_json(collected)
                self.report.collected_items = {
                    _ReconstructedItem(item)  # type: ignore[misc]
                    for item in collected
                }
        self.report.selected_items = selected
        self.report._invalidate_selection_caches()
        warn_selected_collected_mismatch(
            list(self.report.selected_items),
            set(self.report._collected_items_by_nodeid),
        )

    def finish(self) -> int:
        exitstatus = 0
        # Re-sync from config.option in case start() was skipped or option changed.
        set_snapshot_file_lock(
            self.snapshot_file_lock, timeout=self.snapshot_file_lock_timeout
        )
        try:
            self.flush_snapshot_write_queue()
            self.report = SnapshotReport(
                base_dir=self.pytest_session.config.rootpath,
                collected_items=set(self._collected_items.values()),
                selected_items=self._selected_items,
                assertions=self._assertions,
                options=self.pytest_session.config.option,
            )

            if is_xdist_worker():
                # Publish write paths when file locking is on so the controller
                # can remove lock/tmp sidecars after all workers finish.
                if self.snapshot_file_lock:
                    self._publish_write_sidecars()
                # When unused detection is disabled there is nothing for the
                # controller to merge; skip the worker report (5.4-like xdist cost).
                if not self.disable_unused_snapshots:
                    self._publish_worker_report()
                return exitstatus

            # On the pytest-xdist controller no tests run locally, so the report is
            # rebuilt from the reports published by each worker.
            if self._worker_reports:
                self._merge_worker_reports()

            if self.disable_unused_snapshots:
                return exitstatus

            if self.report.num_unused:
                if self.report.should_delete_unused_snapshots:
                    self.remove_unused_snapshots(
                        unused_snapshot_collections=self.report.unused,
                        used_snapshot_collections=self.report.used,
                    )
                elif not self.update_snapshots and not self.warn_unused_snapshots:
                    exitstatus |= EXIT_STATUS_FAIL_UNUSED
            return exitstatus
        finally:
            # Workers must leave lockfiles for siblings still flushing. The
            # controller and single-process runs clean up once writing is done.
            # Also runs on KeyboardInterrupt during finish.
            if self.snapshot_file_lock and not is_xdist_worker():
                self._cleanup_write_sidecars()

    def register_request(self, assertion: "SnapshotAssertion") -> None:
        self._assertions.append(assertion)

        if self.disable_unused_snapshots:
            return

        test_location = assertion.test_location.filepath
        extension_class = assertion.extension.__class__
        if extension_class not in self._locations_discovered[test_location]:
            self._locations_discovered[test_location].add(extension_class)
            discovered_extensions = {
                discovered.location: assertion.extension
                for discovered in assertion.extension.discover_snapshots(
                    test_location=assertion.test_location,
                    ignore_extensions=self.ignore_file_extensions,
                )
                if discovered.has_snapshots
            }
            self._extensions.update(discovered_extensions)

    def remove_unused_snapshots(
        self,
        unused_snapshot_collections: "SnapshotCollections",
        used_snapshot_collections: "SnapshotCollections",
    ) -> None:
        """
        Remove all unused snapshots using the registed extension for the collection file
        If there is not registered extension and the location is unused delete the file
        """
        for unused_snapshot_collection in unused_snapshot_collections:
            snapshot_location = unused_snapshot_collection.location
            if self.snapshot_file_lock:
                # delete_snapshots may create lock sidecars; track for cleanup.
                self._written_snapshot_locations.add(snapshot_location)

            extension = self._extensions.get(snapshot_location)
            if extension:
                extension.delete_snapshots(
                    snapshot_location=snapshot_location,
                    snapshot_names={
                        snapshot.name for snapshot in unused_snapshot_collection
                    },
                )
            elif snapshot_location not in used_snapshot_collections:
                Path(snapshot_location).unlink()

    @staticmethod
    def filter_valid_items(items: list["pytest.Item"]) -> Iterable["pytest.Item"]:
        return (item for item in items if isinstance(item, pytest.Function))
