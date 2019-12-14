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

    def start(self) -> None:
        self.report = []
        self._assertions = []

    def finish(self) -> None:
        (
            _,
            used_snapshots,
            unused_snapshots,
            failed_snapshots,
            created_snapshots,
            updated_snapshots,
            matched_snapshots,
            snapshot_file_assertion,
        ) = self._collate_snapshots()
        n_unused = self._count_snapshots(unused_snapshots)
        n_written = self._count_snapshots(created_snapshots)
        n_updated = self._count_snapshots(updated_snapshots)
        n_failed = self._count_snapshots(failed_snapshots)
        n_passed = self._count_snapshots(matched_snapshots)

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
        if n_written:
            summary_lines += [
                ngettext(
                    "{} snapshot generated.", "{} snapshots generated.", n_written,
                ).format(bold(n_written))
            ]
        if n_unused:
            summary_lines += [
                ngettext(
                    "{} snapshot unused.", "{} snapshots unused.", n_unused
                ).format(yellow(bold(n_unused)))
            ]
        self.add_report_line(" ".join(summary_lines))

        if n_unused:
            self.add_report_line()
            if self.update_snapshots:
                self.remove_unused_snapshots(
                    unused_snapshots, used_snapshots, snapshot_file_assertion
                )
                self.add_report_line(
                    ngettext(
                        "This snapshot has been deleted.",
                        "These snapshots have been deleted.",
                        n_unused,
                    )
                )
                for filepath, snapshots in unused_snapshots.items():
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

    def remove_unused_snapshots(
        self,
        unused_snapshot_files: "SnapshotFiles",
        used_snapshot_files: "SnapshotFiles",
        snapshot_file_assertion: Dict[str, int],
    ) -> None:
        for snapshot_file, unused_snapshots in unused_snapshot_files.items():
            if snapshot_file not in used_snapshot_files:
                os.remove(snapshot_file)
                continue
            snapshot_assertion = self._assertions[
                snapshot_file_assertion[snapshot_file]
            ]
            for snapshot_name in unused_snapshots:
                snapshot_assertion.serializer.delete_snapshot(
                    snapshot_file, snapshot_name
                )

    def _collate_snapshots(
        self,
    ) -> Tuple[
        "SnapshotFiles",
        "SnapshotFiles",
        "SnapshotFiles",
        "SnapshotFiles",
        "SnapshotFiles",
        "SnapshotFiles",
        "SnapshotFiles",
        Dict[str, int],
    ]:
        used_snapshots: "SnapshotFiles" = {}
        failed_snapshots: "SnapshotFiles" = {}
        created_snapshots: "SnapshotFiles" = {}
        updated_snapshots: "SnapshotFiles" = {}
        matched_snapshots: "SnapshotFiles" = {}
        discovered_snapshots: "SnapshotFiles" = {}
        snapshot_file_assertion: Dict[str, int] = {}
        self._merge_snapshot_files_into(
            discovered_snapshots,
            *[assertion.discovered_snapshots for assertion in self._assertions],
        )
        for i, assertion in enumerate(self._assertions):
            for _, result in assertion.executions.items():
                snapshot_file_assertion[result.file] = i
                if used_snapshots.get(result.file):
                    used_snapshots[result.file].add(result.name)
                else:
                    used_snapshots[result.file] = {result.name}
                snapshot_file: "SnapshotFiles" = {result.file: {result.name}}
                if result.created:
                    self._merge_snapshot_files_into(created_snapshots, snapshot_file)
                elif result.updated:
                    self._merge_snapshot_files_into(updated_snapshots, snapshot_file)
                elif result.success:
                    self._merge_snapshot_files_into(matched_snapshots, snapshot_file)
                else:
                    self._merge_snapshot_files_into(failed_snapshots, snapshot_file)

        unused_snapshots: "SnapshotFiles" = self._diff_snapshot_files(
            discovered_snapshots, used_snapshots
        )
        return (
            discovered_snapshots,
            used_snapshots,
            unused_snapshots,
            failed_snapshots,
            created_snapshots,
            updated_snapshots,
            matched_snapshots,
            snapshot_file_assertion,
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
