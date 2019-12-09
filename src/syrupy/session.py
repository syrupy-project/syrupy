import os
from collections import defaultdict
from functools import lru_cache
from gettext import ngettext, gettext
from typing import Dict, List, Set, Tuple, Generator, TYPE_CHECKING

from .constants import SNAPSHOT_DIRNAME
from .terminal import bold, error_style, green, yellow

if TYPE_CHECKING:
    from .assertion import SnapshotAssertion
    from .types import SnapshotFiles


class SnapshotSession:
    def __init__(self, *, update_snapshots: bool, base_dir: str):
        self.update_snapshots = update_snapshots
        self.base_dir = base_dir
        self.discovered_snapshots: "SnapshotFiles" = dict()
        self.visited_snapshots: "SnapshotFiles" = dict()
        self.failed_snapshots: "SnapshotFiles" = dict()
        self.report: List[str] = []
        self._assertions: Dict[str, Dict[str, "SnapshotAssertion"]] = dict()

    @property
    def unused_snapshots(self) -> "SnapshotFiles":
        return self._diff_snapshot_files(
            self.discovered_snapshots, self.visited_snapshots
        )

    @property
    def written_snapshots(self) -> "SnapshotFiles":
        return self._diff_snapshot_files(
            self.visited_snapshots, self.discovered_snapshots
        )

    @property
    def num_unused_snapshots(self) -> int:
        return self._count_snapshots(self.unused_snapshots)

    @property
    def num_written_snapshots(self) -> int:
        return self._count_snapshots(self.written_snapshots)

    def start(self) -> None:
        self.report = []
        self.visited_snapshots = dict()
        self.discovered_snapshots = dict()

    def finish(self) -> None:
        n_unused = self.num_unused_snapshots
        n_written = self.num_written_snapshots
        n_updated = 0  # TODO: self._count_snapshots(self.updated_snapshots)
        n_failed = self._count_snapshots(self.failed_snapshots)
        n_found = self._count_snapshots(self.discovered_snapshots)
        n_passed = n_found - n_unused - n_failed - n_updated

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
        discovered = {
            filepath: assertion.serializer.discover_snapshots(filepath)
            for filepath in self._walk_dir(assertion.serializer.dirname)
        }
        self.add_discovered_snapshots(discovered)

    def register_assertion(self, assertion: "SnapshotAssertion") -> None:
        filepath = assertion.serializer.get_filepath(assertion.num_executions)
        snapshot = assertion.serializer.get_snapshot_name(assertion.num_executions)
        snapshotFile = {filepath: {snapshot}}
        self.add_visited_snapshots(snapshotFile)
        if not assertion.get_assert_result(assertion.num_executions):
            self._merge_snapshot_files_into(self.failed_snapshots, snapshotFile)

        if filepath not in self._assertions:
            self._assertions[filepath] = dict()
        self._assertions[filepath][snapshot] = assertion

    def add_discovered_snapshots(self, snapshots: "SnapshotFiles") -> None:
        self._merge_snapshot_files_into(self.discovered_snapshots, snapshots)

    def add_visited_snapshots(self, snapshots: "SnapshotFiles") -> None:
        self._merge_snapshot_files_into(self.visited_snapshots, snapshots)

    def remove_unused_snapshots(self) -> None:
        for snapshot_file, unused_snapshots in self.unused_snapshots.items():
            all_discovered_unused = (
                unused_snapshots == self.discovered_snapshots[snapshot_file]
            )
            no_snapshot_written = not self.written_snapshots.get(snapshot_file)
            if all_discovered_unused and no_snapshot_written:
                os.remove(snapshot_file)
                continue
            snapshot_assertion, *_ = self._assertions[snapshot_file].values()
            for snapshot_name in unused_snapshots:
                snapshot_assertion.serializer.delete_snapshot(
                    snapshot_file, snapshot_name
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
                if self._in_snapshot_dir(filepath):
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

    def _in_snapshot_dir(self, path: str) -> bool:
        parts = path.split(os.path.sep)
        return SNAPSHOT_DIRNAME in parts

    @lru_cache(maxsize=32)
    def _walk_dir(self, root: str) -> Generator[str, None, None]:
        for (dirpath, _, filenames) in os.walk(root):
            if not self._in_snapshot_dir(dirpath):
                continue
            for filename in filenames:
                if not filename.startswith("."):
                    yield os.path.join(dirpath, filename)
