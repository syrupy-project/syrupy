import json
import os
from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from enum import Enum
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    DefaultDict,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Type,
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


class _FakePytestObject:
    def __init__(self, collected_item: dict[str, str]) -> None:
        self.__module__ = collected_item["modulename"]
        self.__name__ = collected_item["methodname"]


class _FakePytestItem:
    def __init__(self, collected_item: dict[str, str]) -> None:
        self.nodeid = collected_item["nodeid"]
        self.name = collected_item["name"]
        self.path = Path(collected_item["path"])
        self.obj = _FakePytestObject(collected_item)


@dataclass
class SnapshotSession:
    pytest_session: "pytest.Session"
    # Snapshot report generated on finish
    report: Optional["SnapshotReport"] = None
    # All the collected test items
    _collected_items: Set["pytest.Item"] = field(default_factory=set)
    # All the selected test items. Will be set to False until the test item is run.
    _selected_items: Dict[str, ItemStatus] = field(default_factory=dict)
    _assertions: List["SnapshotAssertion"] = field(default_factory=list)
    _extensions: Dict[str, "AbstractSyrupyExtension"] = field(default_factory=dict)

    _locations_discovered: DefaultDict[str, Set[Any]] = field(
        default_factory=lambda: defaultdict(set)
    )

    _queued_snapshot_writes: Dict[
        Tuple[Type["AbstractSyrupyExtension"], str],
        List[Tuple["SerializedData", "PyTestLocation", "SnapshotIndex"]],
    ] = field(default_factory=dict)

    def queue_snapshot_write(
        self,
        extension: "AbstractSyrupyExtension",
        test_location: "PyTestLocation",
        data: "SerializedData",
        index: "SnapshotIndex",
    ) -> None:
        snapshot_location = extension.get_location(
            test_location=test_location, index=index
        )
        key = (extension.__class__, snapshot_location)
        queue = self._queued_snapshot_writes.get(key, [])
        queue.append((data, test_location, index))
        self._queued_snapshot_writes[key] = queue

    def flush_snapshot_write_queue(self) -> None:
        for (
            extension_class,
            snapshot_location,
        ), queued_write in self._queued_snapshot_writes.items():
            if queued_write:
                extension_class.write_snapshot(
                    snapshot_location=snapshot_location, snapshots=queued_write
                )
        self._queued_snapshot_writes = {}

    @property
    def update_snapshots(self) -> bool:
        return bool(self.pytest_session.config.option.update_snapshots)

    @property
    def warn_unused_snapshots(self) -> bool:
        return bool(self.pytest_session.config.option.warn_unused_snapshots)

    def collect_items(self, items: List["pytest.Item"]) -> None:
        self._collected_items.update(self.filter_valid_items(items))

    def select_items(self, items: List["pytest.Item"]) -> None:
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

    def _merge_collected_items(self, collected_items: list[dict[str, str]]) -> None:
        for collected_item in collected_items:
            custom_item = _FakePytestItem(collected_item)
            if not any(
                t.nodeid == custom_item.nodeid and t.name == custom_item.nodeid
                for t in self._collected_items
            ):
                self._collected_items.add(custom_item)  # type: ignore[arg-type]

    def _merge_selected_items(self, selected_items: dict[str, str]) -> None:
        for key, selected_item in selected_items.items():
            if key in self._selected_items:
                status = ItemStatus(selected_item)
                if status != ItemStatus.NOT_RUN:
                    self._selected_items[key] = status
            else:
                self._selected_items[key] = ItemStatus(selected_item)

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
            worker_count = os.getenv("PYTEST_XDIST_WORKER_COUNT")
            with open(".pytest_syrupy_worker_count", "w", encoding="utf-8") as f:
                f.write(worker_count)  # type: ignore[arg-type]
            with open(
                f".pytest_syrupy_{os.getenv("PYTEST_XDIST_WORKER")}_result",
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(self.report.serialize(), f, indent=2)
            return exitstatus
        elif is_xdist_controller():
            # TODO: If we're in a pytest-xdist controller, merge all the reports.
            # Until this is implemented, running syrupy with pytest-xdist is only
            # partially functional.
            return exitstatus

        worker_count = None
        try:
            with open(".pytest_syrupy_worker_count", encoding="utf-8") as f:
                worker_count = f.read()
            os.remove(".pytest_syrupy_worker_count")
        except FileNotFoundError:
            pass

        if worker_count:
            for i in range(int(worker_count)):
                with open(f".pytest_syrupy_gw{i}_result", encoding="utf-8") as f:
                    data = json.load(f)
                    self._merge_collected_items(data["_collected_items"])
                    self._merge_selected_items(data["_selected_items"])
                    self.report.merge_serialized(data)
                os.remove(f".pytest_syrupy_gw{i}_result")

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
                    test_location=assertion.test_location
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
    def filter_valid_items(items: List["pytest.Item"]) -> Iterable["pytest.Item"]:
        return (item for item in items if isinstance(item, pytest.Function))
