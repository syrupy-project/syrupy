import os
from gettext import (
    gettext,
    ngettext,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Generator,
    List,
    Set,
)

import attr

from .data import (
    Snapshot,
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
    from .assertion import SnapshotAssertion  # noqa: F401


@attr.s
class SnapshotReport(object):
    base_dir: str = attr.ib()
    all_items: Set[Any] = attr.ib()
    ran_items: Set[Any] = attr.ib()
    update_snapshots: bool = attr.ib()
    warn_unused_snapshots: bool = attr.ib()
    assertions: List["SnapshotAssertion"] = attr.ib()
    discovered: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    created: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    failed: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    matched: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    updated: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)
    used: "SnapshotFiles" = attr.ib(factory=SnapshotFiles)

    def __attrs_post_init__(self) -> None:
        for assertion in self.assertions:
            self.discovered.merge(assertion.discovered_snapshots)
            for result in assertion.executions.values():
                filepath = result.snapshot_filepath
                snapshot_file = SnapshotFile(filepath=filepath)
                snapshot_file.add(
                    Snapshot(name=result.snapshot_name, data=result.final_data)
                )
                self.used.update(snapshot_file)
                if result.created:
                    self.created.update(snapshot_file)
                elif result.updated:
                    self.updated.update(snapshot_file)
                elif result.success:
                    self.matched.update(snapshot_file)
                else:
                    self.failed.update(snapshot_file)

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
                unused_snapshots = {*unused_snapshot_file}
                mark_file_for_removal = snapshot_filepath not in self.used
            else:
                unused_snapshots = {
                    snapshot
                    for snapshot in unused_snapshot_file
                    if any(
                        TestLocation(node).matches_snapshot_name(snapshot.name)
                        for node in self.ran_items
                    )
                }
                mark_file_for_removal = False

            if unused_snapshots:
                marked_unused_snapshot_file = SnapshotFile(filepath=snapshot_filepath)
                for snapshot in unused_snapshots:
                    marked_unused_snapshot_file.add(snapshot)
                unused_files.add(marked_unused_snapshot_file)
            elif mark_file_for_removal:
                unused_files.add(SnapshotUnknownFile(filepath=snapshot_filepath))
        return unused_files

    @property
    def lines(self) -> Generator[str, None, None]:
        yield ""
        summary_lines: List[str] = []
        if self.num_failed:
            summary_lines.append(
                ngettext(
                    "{} snapshot failed.", "{} snapshots failed.", self.num_failed,
                ).format(error_style(self.num_failed))
            )
        if self.num_matched:
            summary_lines.append(
                ngettext(
                    "{} snapshot passed.", "{} snapshots passed.", self.num_matched,
                ).format(success_style(self.num_matched))
            )
        if self.num_created:
            summary_lines.append(
                ngettext(
                    "{} snapshot generated.",
                    "{} snapshots generated.",
                    self.num_created,
                ).format(green(self.num_created))
            )
        if self.num_updated:
            summary_lines.append(
                ngettext(
                    "{} snapshot updated.", "{} snapshots updated.", self.num_updated,
                ).format(green(self.num_updated))
            )
        if self.num_unused:
            if self.update_snapshots:
                text_singular = "{} unused snapshot deleted."
                text_plural = "{} unused snapshots deleted."
            else:
                text_singular = "{} snapshot unused."
                text_plural = "{} snapshots unused."
            if self.update_snapshots or self.warn_unused_snapshots:
                text_count = warning_style(self.num_unused)
            else:
                text_count = error_style(self.num_unused)
            summary_lines.append(
                ngettext(text_singular, text_plural, self.num_unused).format(text_count)
            )
        yield " ".join(summary_lines)

        if self.num_unused:
            yield ""
            if self.update_snapshots:
                for snapshot_file in self.unused:
                    filepath = snapshot_file.filepath
                    snapshots = (snapshot.name for snapshot in snapshot_file)
                    path_to_file = os.path.relpath(filepath, self.base_dir)
                    deleted_snapshots = ", ".join(map(bold, sorted(snapshots)))
                    yield warning_style(gettext("Deleted {} ({})")).format(
                        deleted_snapshots, path_to_file
                    )
            else:
                message = gettext(
                    "Re-run pytest with --snapshot-update to delete unused snapshots."
                )
                if self.warn_unused_snapshots:
                    yield warning_style(message)
                else:
                    yield error_style(message)

    def _diff_snapshot_files(
        self, snapshot_files1: "SnapshotFiles", snapshot_files2: "SnapshotFiles"
    ) -> "SnapshotFiles":
        diffed_snapshot_files: "SnapshotFiles" = SnapshotFiles()
        for snapshot_file1 in snapshot_files1:
            snapshot_file2 = snapshot_files2.get(
                snapshot_file1.filepath
            ) or SnapshotFile(filepath=snapshot_file1.filepath)
            diffed_snapshot_file = SnapshotFile(filepath=snapshot_file1.filepath)
            for snapshot in snapshot_file1:
                if not snapshot_file2.get(snapshot.name):
                    diffed_snapshot_file.add(snapshot)
            diffed_snapshot_files.add(diffed_snapshot_file)
        return diffed_snapshot_files

    def _count_snapshots(self, snapshot_files: "SnapshotFiles") -> int:
        return sum(len(snapshot_file) for snapshot_file in snapshot_files)
