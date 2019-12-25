import os
from collections import namedtuple
from gettext import (
    gettext,
    ngettext,
)
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
)

from .terminal import (
    bold,
    error_style,
    green,
    success_style,
    warning_style,
)


if TYPE_CHECKING:
    from .assertion import SnapshotAssertion
    from .serializers.base import AbstractSnapshotSerializer  # noqa: F401
    from .types import SnapshotFiles


SnapshotGroups = namedtuple(
    "SnapshotGroups",
    ["created", "discovered", "failed", "matched", "unused", "updated", "used"],
)


def empty_snapshot_groups() -> "SnapshotGroups":
    return SnapshotGroups(
        created={}, discovered={}, failed={}, matched={}, unused={}, updated={}, used={}
    )


class SnapshotSession:
    def __init__(self, *, update_snapshots: bool, base_dir: str):
        self.update_snapshots = update_snapshots
        self.base_dir = base_dir
        self.report: List[str] = []
        self._assertions: List["SnapshotAssertion"] = []
        self._serializers: Dict[str, "AbstractSnapshotSerializer"] = {}
        self._snapshot_groups = empty_snapshot_groups()

    def start(self) -> None:
        self.report = []
        self._assertions = []
        self._serializers = {}
        self._snapshot_groups = empty_snapshot_groups()

    def finish(self) -> None:
        self._collate_snapshots()
        n_unused = self._count_snapshots(self._snapshot_groups.unused)
        n_written = self._count_snapshots(self._snapshot_groups.created)
        n_updated = self._count_snapshots(self._snapshot_groups.updated)
        n_failed = self._count_snapshots(self._snapshot_groups.failed)
        n_passed = self._count_snapshots(self._snapshot_groups.matched)

        self.add_report_line()

        summary_lines: List[str] = []
        if n_failed:
            summary_lines += [
                ngettext(
                    "{} snapshot failed.", "{} snapshots failed.", n_failed
                ).format(error_style(n_failed))
            ]
        if n_passed:
            summary_lines += [
                ngettext(
                    "{} snapshot passed.", "{} snapshots passed.", n_passed
                ).format(success_style(n_passed))
            ]
        if n_written:
            summary_lines += [
                ngettext(
                    "{} snapshot generated.", "{} snapshots generated.", n_written
                ).format(green(n_written))
            ]
        if n_updated:
            summary_lines += [
                ngettext(
                    "{} snapshot updated.", "{} snapshots updated.", n_updated
                ).format(green(n_updated))
            ]
        if n_unused:
            if self.update_snapshots:
                text_singular = "{} snapshot deleted."
                text_plural = "{} snapshots deleted."
            else:
                text_singular = "{} snapshot unused."
                text_plural = "{} snapshots unused."
            text_count = warning_style(n_unused)
            summary_lines += [
                ngettext(text_singular, text_plural, n_unused).format(text_count)
            ]
        self.add_report_line(" ".join(summary_lines))

        if n_unused:
            self.add_report_line()
            if self.update_snapshots:
                self.remove_unused_snapshots(
                    self._snapshot_groups.unused, self._snapshot_groups.used
                )
                for filepath, snapshots in self._snapshot_groups.unused.items():
                    path_to_file = os.path.relpath(filepath, self.base_dir)
                    deleted_snapshots = ", ".join(map(bold, sorted(snapshots)))
                    self.add_report_line(
                        f"Deleted {deleted_snapshots} ({path_to_file})"
                    )
            else:
                self.add_report_line(
                    gettext(
                        "Re-run pytest with --snapshot-update"
                        " to delete the unused snapshots."
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
    ) -> None:
        for snapshot_file, unused_snapshots in unused_snapshot_files.items():
            for snapshot_name in unused_snapshots:
                self._serializers[snapshot_file].delete_snapshot(
                    snapshot_file, snapshot_name
                )
            if (
                os.path.exists(snapshot_file)
                and snapshot_file not in used_snapshot_files
            ):
                os.remove(snapshot_file)

    def _collate_snapshots(self) -> None:
        """
        Prepare session for snapshot reporting
        """
        for assertion in self._assertions:
            self._merge_snapshot_files_into(
                self._snapshot_groups.discovered, assertion.discovered_snapshots
            )
            for filepath in assertion.discovered_snapshots:
                self._serializers[filepath] = assertion.serializer
            for result in assertion.executions.values():
                snapshot_file: "SnapshotFiles" = {result.file: {result.name}}
                self._merge_snapshot_files_into(
                    self._snapshot_groups.used, snapshot_file
                )
                if result.created:
                    self._merge_snapshot_files_into(
                        self._snapshot_groups.created, snapshot_file
                    )
                elif result.updated:
                    self._merge_snapshot_files_into(
                        self._snapshot_groups.updated, snapshot_file
                    )
                elif result.success:
                    self._merge_snapshot_files_into(
                        self._snapshot_groups.matched, snapshot_file
                    )
                else:
                    self._merge_snapshot_files_into(
                        self._snapshot_groups.failed, snapshot_file
                    )

        unused_snapshot_files = {
            snapshot_file: unused_snapshots
            for snapshot_file, unused_snapshots in self._diff_snapshot_files(
                self._snapshot_groups.discovered, self._snapshot_groups.used
            ).items()
            if unused_snapshots
        }
        self._snapshot_groups.unused.update(unused_snapshot_files)

    def _merge_snapshot_files_into(
        self, snapshot_files: "SnapshotFiles", *snapshot_files_to_merge: "SnapshotFiles"
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
        self, snapshot_files1: "SnapshotFiles", snapshot_files2: "SnapshotFiles"
    ) -> "SnapshotFiles":
        return {
            filename: snapshots1 - snapshot_files2.get(filename, set())
            for filename, snapshots1 in snapshot_files1.items()
        }

    def _count_snapshots(self, snapshot_files: "SnapshotFiles") -> int:
        return sum(len(snaps) for snaps in snapshot_files.values())
