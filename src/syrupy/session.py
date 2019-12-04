import os
from collections import defaultdict
from functools import lru_cache
from gettext import ngettext, gettext
from typing import Dict, List, Set, Tuple

from .assertion import SnapshotAssertion
from .constants import SNAPSHOT_DIRNAME
from .terminal import yellow, bold
from .types import SnapshotFiles


class SnapshotSession:
    def __init__(self, *, update_snapshots: bool, base_dir: str):
        self.update_snapshots = update_snapshots
        self.base_dir = base_dir
        self.discovered_snapshots: SnapshotFiles = dict()
        self.visited_snapshots: SnapshotFiles = dict()
        self.report: List[str] = []
        self._assertions: Dict[str, Dict[str, SnapshotAssertion]] = dict()

    @property
    def unused_snapshots(self) -> SnapshotFiles:
        return self._diff_snapshot_files(
            self.discovered_snapshots, self.visited_snapshots
        )

    @property
    def written_snapshots(self) -> SnapshotFiles:
        return self._diff_snapshot_files(
            self.visited_snapshots, self.discovered_snapshots
        )

    @property
    def num_unused_snapshots(self):
        return self._count_snapshots(self.unused_snapshots)

    @property
    def num_written_snapshots(self):
        return self._count_snapshots(self.written_snapshots)

    def start(self):
        self.report = []
        self.visited_snapshots = dict()
        self.discovered_snapshots = dict()

    def finish(self):
        n_unused = self.num_unused_snapshots
        n_written = self.num_written_snapshots

        self.add_report_line()

        summary_lines = []
        if self.update_snapshots and n_written:
            summary_lines += [
                ngettext(
                    "{} snapshot generated.", "{} snapshots generated.", n_written,
                ).format(bold(n_written))
            ]
        summary_lines += [
            ngettext("{} snapshot unused.", "{} snapshots unused.", n_unused).format(
                bold(n_unused)
            )
        ]
        summary_line = " ".join(summary_lines)
        self.add_report_line(
            yellow(summary_line)
            if n_unused or (self.update_snapshots and n_written)
            else summary_line
        )

        for filepath, snapshots in self.unused_snapshots.items():
            count = self._count_snapshots({filepath: snapshots})
            if not count:
                continue
            path_to_file = os.path.relpath(filepath, self.base_dir)
            self.add_report_line(
                ngettext(
                    f"{{}} at {path_to_file}",
                    f"{{}} in {path_to_file} → {', '.join(snapshots)}",
                    count,
                ).format(bold(count))
            )

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
            else:
                self.add_report_line(
                    gettext(
                        "Re-run pytest with --update-snapshots to delete the snapshots."
                    )
                )

    def add_report_line(self, line: str = ""):
        self.report += [line]

    def register_request(self, assertion: SnapshotAssertion):
        discovered = {
            filepath: assertion.io.discover_snapshots(filepath)
            for filepath in self._walk_dir(assertion.io.dirname)
        }
        self.add_discovered_snapshots(discovered)

    def register_assertion(self, assertion: SnapshotAssertion):
        filepath = assertion.io.get_filepath(assertion.num_executions)
        snapshot = assertion.io.get_snapshot_name(assertion.num_executions)
        self.add_visited_snapshots({filepath: {snapshot}})

        if filepath not in self._assertions:
            self._assertions[filepath] = dict()
        self._assertions[filepath][snapshot] = assertion

    def add_discovered_snapshots(self, snapshots: SnapshotFiles):
        self._merge_snapshot_files_into(self.discovered_snapshots, snapshots)

    def add_visited_snapshots(self, snapshots: SnapshotFiles):
        self._merge_snapshot_files_into(self.visited_snapshots, snapshots)

    def remove_unused_snapshots(self):
        for snapshot_file, unused_snapshots in self.unused_snapshots.items():
            if self.discovered_snapshots[snapshot_file] == unused_snapshots:
                os.remove(snapshot_file)
                continue
            snapshot_assertion, *_ = self._assertions[snapshot_file].values()
            for snapshot_name in unused_snapshots:
                snapshot_assertion.io.delete_snapshot(snapshot_file, snapshot_name)

    def _merge_snapshot_files_into(
        self, snapshot_files: SnapshotFiles, *snapshot_files_to_merge: SnapshotFiles,
    ):
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
        self, snapshot_files1: SnapshotFiles, snapshot_files2: SnapshotFiles,
    ) -> SnapshotFiles:
        return {
            filename: snapshots1 - snapshot_files2.get(filename, set())
            for filename, snapshots1 in snapshot_files1.items()
        }

    def _count_snapshots(self, snapshot_files: SnapshotFiles) -> int:
        return sum(len(snaps) for snaps in snapshot_files.values())

    def _in_snapshot_dir(self, path: str) -> bool:
        parts = path.split(os.path.sep)
        return SNAPSHOT_DIRNAME in parts

    @lru_cache(maxsize=32)
    def _walk_dir(self, root: str):
        for (dirpath, _, filenames) in os.walk(root):
            if not self._in_snapshot_dir(dirpath):
                continue
            for filename in filenames:
                if not filename.startswith("."):
                    yield os.path.join(dirpath, filename)
