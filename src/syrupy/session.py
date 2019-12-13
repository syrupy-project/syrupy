import os
from collections import defaultdict
from functools import lru_cache
from gettext import (
    gettext,
    ngettext,
)
from typing import (
    TYPE_CHECKING,
    Dict,
    Generator,
    List,
    Set,
    Tuple,
)

from .constants import SNAPSHOT_DIRNAME
from .terminal import (
    bold,
    error_style,
    green,
    yellow,
)


if TYPE_CHECKING:
    from .assertion import SnapshotAssertion
    from .types import SnapshotFiles


class SnapshotSession:
    def __init__(self, *, update_snapshots: bool, base_dir: str):
        self.update_snapshots = update_snapshots
        self.base_dir = base_dir
        self.report: List[str] = []
        self._assertions: List["SnapshotAssertion"] = []

    @property
    def unused_snapshots(self) -> "SnapshotFiles":
        return {}

    @property
    def written_snapshots(self) -> "SnapshotFiles":
        return {}

    @property
    def num_unused_snapshots(self) -> int:
        return 0

    @property
    def num_written_snapshots(self) -> int:
        return 0

    def start(self) -> None:
        self.report = []
        self._assertions = []

    def finish(self) -> None:
        n_unused = self.num_unused_snapshots
        n_written = self.num_written_snapshots
        n_updated = 0  # TODO
        n_failed = 0  # TODO
        n_found = 0  # TODO
        n_passed = n_found - n_unused - n_failed - n_updated  # TODO

        self.add_report_line()

        summary_lines: List[str] = []
        if n_failed:
            summary_lines += [
                ngettext(
                    "{} snapshot failed.", "{} snapshots failed.", n_failed,
                ).format(error_style(n_failed))
            ]
        if n_passed:
            summary_lines += [
                ngettext(
                    "{} snapshot passed.", "{} snapshots passed.", n_passed,
                ).format(green(bold(n_passed)))
            ]
        if n_updated:
            summary_lines += [
                ngettext(
                    "{} snapshot updated.", "{} snapshots updated.", n_passed,
                ).format(bold(n_passed))
            ]
        if self.update_snapshots and n_written:
            summary_lines += [
                ngettext(
                    "{} snapshot generated.", "{} snapshots generated.", n_written,
                ).format(bold(n_written))
            ]
        if not self.update_snapshots and n_unused:
            summary_lines += [
                ngettext(
                    "{} snapshot unused.", "{} snapshots unused.", n_unused
                ).format(yellow(bold(n_unused)))
            ]
        self.add_report_line(" ".join(summary_lines))

        if n_unused:
            self.add_report_line()
            if self.update_snapshots:
                self.remove_unused_snapshots()
                self.add_report_line(
                    ngettext(
                        "This snapshot has been deleted.",
                        "These snapshots have been deleted.",
                        n_unused,
                    )
                )
                for filepath, snapshots in self.unused_snapshots.items():
                    count = self._count_snapshots({filepath: snapshots})
                    if not count:
                        continue
                    path_to_file = os.path.relpath(filepath, self.base_dir)
                    self.add_report_line(
                        f"{', '.join(sorted(snapshots))} → {path_to_file}"
                    )
            else:
                self.add_report_line(
                    gettext(
                        "Re-run pytest with --snapshot-update to delete the snapshots."
                    )
                )

    def add_report_line(self, line: str = "") -> None:
        self.report += [line]

    def register_request(self, assertion: "SnapshotAssertion") -> None:
        self._assertions.append(assertion)

    def remove_unused_snapshots(self) -> None:
        pass

    def _merge_snapshot_files_into(
        self,
        snapshot_files: "SnapshotFiles",
        *snapshot_files_to_merge: "SnapshotFiles",
    ) -> None:
        """
        Add snapshots from other files into the first one
        """
        for snapshot_file in snapshot_files_to_merge:
            for filepath, snapshots in snapshot_file.items():
                if filepath not in snapshot_files:
                    snapshot_files[filepath] = set()
                snapshot_files[filepath].update(snapshots)

    def _diff_snapshot_files(
        self, snapshot_files1: "SnapshotFiles", snapshot_files2: "SnapshotFiles",
    ) -> "SnapshotFiles":
        return {
            filename: snapshots1 - snapshot_files2.get(filename, set())
            for filename, snapshots1 in snapshot_files1.items()
        }

    def _count_snapshots(self, snapshot_files: "SnapshotFiles") -> int:
        return sum(len(snaps) for snaps in snapshot_files.values())
