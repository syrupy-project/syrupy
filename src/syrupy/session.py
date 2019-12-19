import os
from collections import defaultdict
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

    def start(self) -> None:
        self.report = []
        self._assertions = []

    def finish(self) -> None:
        self._collate_snapshots()
        n_unused = self._count_snapshots(self._unused_snapshots)
        n_written = self._count_snapshots(self._created_snapshots)
        n_updated = self._count_snapshots(self._updated_snapshots)
        n_failed = self._count_snapshots(self._failed_snapshots)
        n_passed = self._count_snapshots(self._matched_snapshots)

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
        if n_written:
            summary_lines += [
                ngettext(
                    "{} snapshot generated.", "{} snapshots generated.", n_written,
                ).format(green(n_written))
            ]
        if n_updated:
            summary_lines += [
                ngettext(
                    "{} snapshot updated.", "{} snapshots updated.", n_updated,
                ).format(green(n_updated))
            ]
        if n_unused:
            if self.update_snapshots:
                text_singular = "{} snapshot deleted."
                text_plural = "{} snapshots deleted."
            else:
                text_singular = "{} snapshot unused."
                text_plural = "{} snapshots unused."
            text_count = yellow(bold(n_unused))
            summary_lines += [
                ngettext(text_singular, text_plural, n_unused).format(text_count)
            ]
        self.add_report_line(" ".join(summary_lines))

        if n_unused:
            self.add_report_line()
            if self.update_snapshots:
                self.remove_unused_snapshots(
                    self._unused_snapshots,
                    self._used_snapshots,
                    self._snapshot_assertions,
                )
                for filepath, snapshots in self._unused_snapshots.items():
                    count = self._count_snapshots({filepath: snapshots})
                    if not count:
                        continue
                    path_to_file = os.path.relpath(filepath, self.base_dir)
                    self.add_report_line(
                        f"Deleted {', '.join(map(bold, sorted(snapshots)))} ({path_to_file})"
                    )
            else:
                self.add_report_line(
                    gettext(
                        "Re-run pytest with --snapshot-update to delete the unused snapshots."
                    )
                )

    def add_report_line(self, line: str = "") -> None:
        self.report += [line]

    def register_request(self, assertion: "SnapshotAssertion") -> None:
        self._assertions.append(assertion)

    def remove_unused_snapshots(
        self,
        unused_snapshot_files: "SnapshotFiles",
        used_snapshot_files: "SnapshotFiles",
        snapshot_assertions: Dict[str, "SnapshotAssertion"],
    ) -> None:
        for snapshot_file, unused_snapshots in unused_snapshot_files.items():
            if snapshot_file not in used_snapshot_files:
                os.remove(snapshot_file)
                continue
            for snapshot_name in unused_snapshots:
                self._snapshot_assertions[snapshot_file].serializer.delete_snapshot(
                    snapshot_file, snapshot_name
                )

    def _collate_snapshots(self) -> None:
        """
        Prepare session for snapshot reporting
        """
        self._used_snapshots: "SnapshotFiles" = {}
        self._failed_snapshots: "SnapshotFiles" = {}
        self._created_snapshots: "SnapshotFiles" = {}
        self._updated_snapshots: "SnapshotFiles" = {}
        self._matched_snapshots: "SnapshotFiles" = {}
        self._discovered_snapshots: "SnapshotFiles" = {}
        self._snapshot_assertions: Dict[str, "SnapshotAssertion"] = {}
        for assertion in self._assertions:
            self._merge_snapshot_files_into(
                self._discovered_snapshots, assertion.discovered_snapshots
            )
            for result in assertion.executions.values():
                self._snapshot_assertions[result.file] = assertion
                snapshot_file: "SnapshotFiles" = {result.file: {result.name}}
                self._merge_snapshot_files_into(self._used_snapshots, snapshot_file)
                if result.created:
                    self._merge_snapshot_files_into(
                        self._created_snapshots, snapshot_file
                    )
                elif result.updated:
                    self._merge_snapshot_files_into(
                        self._updated_snapshots, snapshot_file
                    )
                elif result.success:
                    self._merge_snapshot_files_into(
                        self._matched_snapshots, snapshot_file
                    )
                else:
                    self._merge_snapshot_files_into(
                        self._failed_snapshots, snapshot_file
                    )

        self._unused_snapshots: "SnapshotFiles" = self._diff_snapshot_files(
            self._discovered_snapshots, self._used_snapshots
        )

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
