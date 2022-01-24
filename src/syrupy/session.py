from collections import defaultdict
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    DefaultDict,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
)

import attr
import pytest

from .constants import EXIT_STATUS_FAIL_UNUSED
from .data import SnapshotFossils
from .report import SnapshotReport

if TYPE_CHECKING:
    from .assertion import SnapshotAssertion
    from .extensions.base import AbstractSyrupyExtension


@attr.s
class SnapshotSession:
    # pytest.Session
    _pytest_session: Any = attr.ib()
    # Snapshot report generated on finish
    report: Optional["SnapshotReport"] = attr.ib(default=None)
    # All the collected test items
    _collected_items: Set["pytest.Item"] = attr.ib(factory=set)
    # All the selected test items. Will be set to False until the test item is run.
    _selected_items: Dict[str, bool] = attr.ib(factory=dict)
    _assertions: List["SnapshotAssertion"] = attr.ib(factory=list)
    _extensions: Dict[str, "AbstractSyrupyExtension"] = attr.ib(factory=dict)

    _locations_discovered: DefaultDict[str, Set[Any]] = attr.ib(
        factory=lambda: defaultdict(set)
    )

    @property
    def update_snapshots(self) -> bool:
        return bool(self._pytest_session.config.option.update_snapshots)

    @property
    def warn_unused_snapshots(self) -> bool:
        return bool(self._pytest_session.config.option.warn_unused_snapshots)

    def collect_items(self, items: List["pytest.Item"]) -> None:
        self._collected_items.update(self.filter_valid_items(items))

    def select_items(self, items: List["pytest.Item"]) -> None:
        for item in self.filter_valid_items(items):
            self._selected_items[getattr(item, "nodeid")] = False  # noqa: B009

    def start(self) -> None:
        self.report = None
        self._collected_items = set()
        self._selected_items = {}
        self._assertions = []
        self._extensions = {}
        self._locations_discovered = defaultdict(set)

    def ran_item(self, nodeid: str) -> None:
        if nodeid in self._selected_items:
            self._selected_items[nodeid] = True

    def finish(self) -> int:
        exitstatus = 0
        self.report = SnapshotReport(
            base_dir=self._pytest_session.config.rootdir,
            collected_items=self._collected_items,
            selected_items=self._selected_items,
            assertions=self._assertions,
            options=self._pytest_session.config.option,
        )
        if self.report.num_unused:
            if self.update_snapshots:
                self.remove_unused_snapshots(
                    unused_snapshot_fossils=self.report.unused,
                    used_snapshot_fossils=self.report.used,
                )
            elif not self.warn_unused_snapshots:
                exitstatus |= EXIT_STATUS_FAIL_UNUSED
        return exitstatus

    def register_request(self, assertion: "SnapshotAssertion") -> None:
        self._assertions.append(assertion)

        test_location = assertion.extension.test_location.filepath
        extension_class = assertion.extension.__class__
        if extension_class not in self._locations_discovered[test_location]:
            self._locations_discovered[test_location].add(extension_class)
            discovered_extensions = {
                discovered.location: assertion.extension
                for discovered in assertion.extension.discover_snapshots()
                if discovered.has_snapshots
            }
            self._extensions.update(discovered_extensions)

    def remove_unused_snapshots(
        self,
        unused_snapshot_fossils: "SnapshotFossils",
        used_snapshot_fossils: "SnapshotFossils",
    ) -> None:
        """
        Remove all unused snapshots using the registed extension for the fossil file
        If there is not registered extension and the location is unused delete the file
        """
        for unused_snapshot_fossil in unused_snapshot_fossils:
            snapshot_location = unused_snapshot_fossil.location

            extension = self._extensions.get(snapshot_location)
            if extension:
                extension.delete_snapshots(
                    snapshot_location=snapshot_location,
                    snapshot_names={
                        snapshot.name for snapshot in unused_snapshot_fossil
                    },
                )
            elif snapshot_location not in used_snapshot_fossils:
                Path(snapshot_location).unlink()

    @staticmethod
    def filter_valid_items(items: List["pytest.Item"]) -> Iterable["pytest.Item"]:
        return (item for item in items if isinstance(item, pytest.Function))
