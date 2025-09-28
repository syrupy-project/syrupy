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
from .location import PyTestLocation
from .report import SnapshotReport
from .types import (
    SerializedData,
    SnapshotIndex,
)
from .utils import (
    is_xdist_controller,
    is_xdist_worker,
)

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
    # All the collected test items
    _collected_items: set["pytest.Item"] = field(default_factory=set)
    # All the selected test items. Will be set to False until the test item is run.
    _selected_items: dict[str, ItemStatus] = field(default_factory=dict)
    _assertions: list["SnapshotAssertion"] = field(default_factory=list)
    _extensions: dict[str, "AbstractSyrupyExtension"] = field(default_factory=dict)

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

    def flush_snapshot_write_queue(self) -> None:
        for (
            extension_class,
            snapshot_location,
        ), queued_write in self._queued_snapshot_writes.items():
            if queued_write:
                extension_class.write_snapshot(
                    snapshot_location=snapshot_location,
                    snapshots=[
                        (data, loc, index)
                        for (loc, index), data in queued_write.items()
                    ],
                )
        self._queued_snapshot_writes.clear()

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

    def collect_items(self, items: list["pytest.Item"]) -> None:
        self._collected_items.update(self.filter_valid_items(items))

    def select_items(self, items: list["pytest.Item"]) -> None:
        for item in self.filter_valid_items(items):
            self._selected_items[getattr(item, "nodeid")] = (  # noqa: B009
                ItemStatus.NOT_RUN
            )

    def start(self) -> None:
        self.report = None
        self._collected_items = set()
        self._selected_items = {}
        self._assertions = []
        self._extensions = {}
        self._locations_discovered = defaultdict(set)

    def ran_item(
        self, nodeid: str, outcome: Literal["passed", "skipped", "failed"]
    ) -> None:
        if nodeid in self._selected_items:
            try:
                self._selected_items[nodeid] = ItemStatus(outcome)
            except ValueError:
                pass  # if we don't understand the outcome, leave the item as "not run"

    def finish(self) -> int:
        exitstatus = 0
        self.flush_snapshot_write_queue()
        self.report = SnapshotReport(
            base_dir=self.pytest_session.config.rootpath,
            collected_items=self._collected_items,
            selected_items=self._selected_items,
            assertions=self._assertions,
            options=self.pytest_session.config.option,
        )

        if is_xdist_worker():
            # TODO: If we're in a pytest-xdist worker, we need to combine the reports
            #  of all the workers so that the controller can handle unused
            #  snapshot removal.
            return exitstatus
        elif is_xdist_controller():
            # TODO: If we're in a pytest-xdist controller, merge all the reports.
            #  Until this is implemented, running syrupy with pytest-xdist is only
            #  partially functional.
            return exitstatus

        if self.report.num_unused:
            if self.update_snapshots:
                self.remove_unused_snapshots(
                    unused_snapshot_collections=self.report.unused,
                    used_snapshot_collections=self.report.used,
                )
            elif not self.warn_unused_snapshots:
                exitstatus |= EXIT_STATUS_FAIL_UNUSED
        return exitstatus

    def register_request(self, assertion: "SnapshotAssertion") -> None:
        self._assertions.append(assertion)

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
