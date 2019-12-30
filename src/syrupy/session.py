import os
from gettext import (
    gettext,
    ngettext,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Set,
)

import attr

from .constants import EXIT_STATUS_FAIL_UNUSED
from .data import (
    SnapshotData,
    SnapshotFile,
    SnapshotFiles,
    SnapshotUnknownFile,
)
from .location import TestLocation
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


@attr.s
class SnapshotReportingGroups(object):
    all_items: Set[Any] = attr.ib()
    ran_items: Set[Any] = attr.ib()
    discovered: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    created: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    failed: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    matched: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    updated: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    used: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)

    @property
    def num_created(self) -> int:
        return self._count_snapshots(self.created)

    @property
    def num_failed(self) -> int:
        return self._count_snapshots(self.failed)

    @property
    def num_matched(self) -> int:
        return self._count_snapshots(self.matched)

    @property
    def num_updated(self) -> int:
        return self._count_snapshots(self.updated)

    @property
    def num_unused(self) -> int:
        return self._count_snapshots(self.unused)

    @property
    def ran_all_collected_tests(self) -> bool:
        return self.all_items == self.ran_items

    @property
    def unused(self) -> "SnapshotFiles":
        unused_files = SnapshotFiles()
        for unused_snapshot_file in self._diff_snapshot_files(
            self.discovered, self.used
        ):
            snapshot_filepath = unused_snapshot_file.filepath
            if self.ran_all_collected_tests:
                unused_snapshots = dict(unused_snapshot_file.snapshots)
                mark_file_for_removal = snapshot_filepath not in self.used
            else:
                unused_snapshots = {
                    snapshot_name: unused_snapshot_file.snapshots[snapshot_name]
                    for snapshot_name in unused_snapshot_file.snapshots
                    if any(
                        TestLocation(node).matches_snapshot_name(snapshot_name)
                        for node in self.ran_items
                    )
                }
                mark_file_for_removal = False

            if unused_snapshots:
                marked_unused_snapshot_file = SnapshotFile(
                    filepath=snapshot_filepath, snapshots=unused_snapshots
                )
                unused_files.add(marked_unused_snapshot_file)
            elif mark_file_for_removal:
                unused_files.add(SnapshotUnknownFile(filepath=snapshot_filepath))
        return unused_files

    def _diff_snapshot_files(
        self, snapshot_files1: "SnapshotFiles", snapshot_files2: "SnapshotFiles"
    ) -> "SnapshotFiles":
        diffed_snapshot_files: "SnapshotFiles" = SnapshotFiles()
        for snapshot_file1 in snapshot_files1:
            snapshot_file2 = snapshot_files2.get(
                snapshot_file1.filepath
            ) or SnapshotFile(filepath=snapshot_file1.filepath)
            diffed_snapshots = {
                snapshot_name: snapshot_file1.snapshots[snapshot_name]
                for snapshot_name in (
                    snapshot_file1.snapshots.keys() - snapshot_file2.snapshots.keys()
                )
            }
            diffed_snapshot_files.add(
                SnapshotFile(
                    filepath=snapshot_file1.filepath, snapshots=diffed_snapshots
                )
            )
        return diffed_snapshot_files

    def _count_snapshots(self, snapshot_files: "SnapshotFiles") -> int:
        return sum(len(snapshot_file.snapshots) for snapshot_file in snapshot_files)


class SnapshotSession:
    def __init__(
        self, *, warn_unused_snapshots: bool, update_snapshots: bool, base_dir: str
    ):
        self.warn_unused_snapshots = warn_unused_snapshots
        self.update_snapshots = update_snapshots
        self.base_dir = base_dir
        self.report: List[str] = []
        self._all_items: Set[Any] = set()
        self._ran_items: Set[Any] = set()
        self._assertions: List["SnapshotAssertion"] = []
        self._serializers: Dict[str, "AbstractSnapshotSerializer"] = {}

    def start(self) -> None:
        self.report = []
        self._all_items = set()
        self._ran_items = set()
        self._assertions = []
        self._serializers = {}

    def finish(self) -> int:
        exitstatus = 0
        snapshot_groups = self._get_snapshot_groups()
        self.add_report_line()

        summary_lines: List[str] = []
        if snapshot_groups.num_failed:
            summary_lines += [
                ngettext(
                    "{} snapshot failed.",
                    "{} snapshots failed.",
                    snapshot_groups.num_failed,
                ).format(error_style(snapshot_groups.num_failed))
            ]
        if snapshot_groups.num_matched:
            summary_lines += [
                ngettext(
                    "{} snapshot passed.",
                    "{} snapshots passed.",
                    snapshot_groups.num_matched,
                ).format(success_style(snapshot_groups.num_matched))
            ]
        if snapshot_groups.num_created:
            summary_lines += [
                ngettext(
                    "{} snapshot generated.",
                    "{} snapshots generated.",
                    snapshot_groups.num_created,
                ).format(green(snapshot_groups.num_created))
            ]
        if snapshot_groups.num_updated:
            summary_lines += [
                ngettext(
                    "{} snapshot updated.",
                    "{} snapshots updated.",
                    snapshot_groups.num_updated,
                ).format(green(snapshot_groups.num_updated))
            ]
        if snapshot_groups.num_unused:
            if self.update_snapshots:
                text_singular = "{} unused snapshot deleted."
                text_plural = "{} unused snapshots deleted."
            else:
                text_singular = "{} snapshot unused."
                text_plural = "{} snapshots unused."
            if self.update_snapshots or self.warn_unused_snapshots:
                text_count = warning_style(snapshot_groups.num_unused)
            else:
                text_count = error_style(snapshot_groups.num_unused)
            summary_lines += [
                ngettext(text_singular, text_plural, snapshot_groups.num_unused).format(
                    text_count
                )
            ]
        self.add_report_line(" ".join(summary_lines))

        if snapshot_groups.num_unused:
            self.add_report_line()
            unused_snapshot_files = snapshot_groups.unused
            if self.update_snapshots:
                self.remove_unused_snapshots(
                    unused_snapshot_files, snapshot_groups.used
                )
                for snapshot_file in unused_snapshot_files:
                    filepath = snapshot_file.filepath
                    snapshots = snapshot_file.snapshots
                    path_to_file = os.path.relpath(filepath, self.base_dir)
                    deleted_snapshots = ", ".join(map(bold, sorted(snapshots)))
                    self.add_report_line(
                        gettext(f"Deleted {deleted_snapshots} ({path_to_file})")
                    )
            else:
                message = gettext(
                    "Re-run pytest with --snapshot-update"
                    " to delete the unused snapshots."
                )
                if self.warn_unused_snapshots:
                    message = warning_style(message)
                else:
                    message = error_style(message)
                    exitstatus |= EXIT_STATUS_FAIL_UNUSED
                self.add_report_line(message)
        return exitstatus

    def add_report_line(self, line: str = "") -> None:
        self.report += [line]

    def register_request(self, assertion: "SnapshotAssertion") -> None:
        self._assertions.append(assertion)

    def remove_unused_snapshots(
        self,
        unused_snapshot_files: "SnapshotFiles",
        used_snapshot_files: "SnapshotFiles",
    ) -> None:
        for unused_snapshot_file in unused_snapshot_files:
            snapshot_file = unused_snapshot_file.filepath
            unused_snapshots = set(unused_snapshot_file.snapshots.keys())
            serializer = self._serializers.get(snapshot_file)
            if serializer:
                serializer.delete_snapshots_from_file(snapshot_file, unused_snapshots)
            elif snapshot_file not in used_snapshot_files:
                os.remove(snapshot_file)

    def _get_snapshot_groups(self) -> "SnapshotReportingGroups":
        """
        Prepare snapshot groups for session reporting
        """
        snapshot_groups = SnapshotReportingGroups(
            all_items=self._all_items, ran_items=self._ran_items
        )
        for assertion in self._assertions:
            for discovered in assertion.discovered_snapshots:
                snapshot_groups.discovered.merge(discovered)
                if discovered.has_snapshots:
                    self._serializers[discovered.filepath] = assertion.serializer
            for result in assertion.executions.values():
                snapshot_file = SnapshotFile(
                    filepath=result.file,
                    snapshots={result.name: SnapshotData(data=result.final_data)},
                )
                snapshot_groups.used.merge(snapshot_file)
                if result.created:
                    snapshot_groups.created.merge(snapshot_file)
                elif result.updated:
                    snapshot_groups.updated.merge(snapshot_file)
                elif result.success:
                    snapshot_groups.matched.merge(snapshot_file)
                else:
                    snapshot_groups.failed.merge(snapshot_file)
        return snapshot_groups
