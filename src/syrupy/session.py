import os
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Set,
)

from .constants import EXIT_STATUS_FAIL_UNUSED
from .data import SnapshotCaches
from .report import SnapshotReport


if TYPE_CHECKING:
    from .assertion import SnapshotAssertion
    from .extensions.base import AbstractSyrupyExtension  # noqa: F401


class SnapshotSession:
    def __init__(
        self, *, warn_unused_snapshots: bool, update_snapshots: bool, base_dir: str
    ):
        self.warn_unused_snapshots = warn_unused_snapshots
        self.update_snapshots = update_snapshots
        self.base_dir = base_dir
        self.report: Optional["SnapshotReport"] = None
        self._all_items: Set[Any] = set()
        self._ran_items: Set[Any] = set()
        self._assertions: List["SnapshotAssertion"] = []
        self._extensions: Dict[str, "AbstractSyrupyExtension"] = {}

    def start(self) -> None:
        self.report = None
        self._all_items = set()
        self._ran_items = set()
        self._assertions = []
        self._extensions = {}

    def finish(self) -> int:
        exitstatus = 0
        self.report = SnapshotReport(
            base_dir=self.base_dir,
            all_items=self._all_items,
            ran_items=self._ran_items,
            assertions=self._assertions,
            update_snapshots=self.update_snapshots,
            warn_unused_snapshots=self.warn_unused_snapshots,
        )
        if self.report.num_unused:
            if self.update_snapshots:
                self.remove_unused_snapshots(
                    unused_snapshot_caches=self.report.unused,
                    used_snapshot_caches=self.report.used,
                )
            elif not self.warn_unused_snapshots:
                exitstatus |= EXIT_STATUS_FAIL_UNUSED
        return exitstatus

    def register_request(self, assertion: "SnapshotAssertion") -> None:
        self._assertions.append(assertion)
        discovered_extensions = {
            discovered.location: assertion.extension
            for discovered in assertion.extension.discover_snapshots()
            if discovered.has_snapshots
        }
        self._extensions.update(discovered_extensions)

    def remove_unused_snapshots(
        self,
        unused_snapshot_caches: "SnapshotCaches",
        used_snapshot_caches: "SnapshotCaches",
    ) -> None:
        for unused_snapshot_cache in unused_snapshot_caches:
            snapshot_cache = unused_snapshot_cache.location
            extension = self._extensions.get(snapshot_cache)
            if extension:
                extension.delete_snapshots_from_file(
                    snapshot_cache,
                    {snapshot.name for snapshot in unused_snapshot_cache},
                )
            elif snapshot_cache not in used_snapshot_caches:
                os.remove(snapshot_cache)
