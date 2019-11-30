import os
from collections import defaultdict
from gettext import ngettext, gettext
from typing import Dict, List, Set, Tuple

from .assertion import SnapshotAssertion
from .constants import SNAPSHOT_DIRNAME
from .terminal import yellow, bold
from .types import Albums


class SnapshotSession:
    def __init__(self, *, update_snapshots: bool, base_dir: str):
        self.update_snapshots = update_snapshots
        self.base_dir = base_dir
        self.discovered_albums: Albums = dict()
        self.visited_albums: Albums = dict()
        self.report: List[str] = []
        self._assertions: Dict[str, Dict[str, SnapshotAssertion]] = dict()

    @property
    def unused_snapshots(self) -> Albums:
        return self._subtract_albums(self.discovered_albums, self.visited_albums)

    @property
    def written_snapshots(self) -> Albums:
        return self._subtract_albums(self.visited_albums, self.discovered_albums)

    @property
    def num_unused_snapshots(self):
        return self._count_snapshots(self.unused_snapshots)

    @property
    def num_written_snapshots(self):
        return self._count_snapshots(self.written_snapshots)

    def start(self):
        self.report = []
        self.visited_albums = dict()
        self.discovered_albums = dict()

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
        self.add_discovered_snapshots(
            {filepath: set() for filepath in self._walk_dir(assertion.io.dirname)}
        )

    def register_assertion(self, assertion: SnapshotAssertion, executions: int = 0):
        self.add_discovered_snapshots(assertion.io.discover_snapshots(executions))

        filepath = assertion.io.get_filepath(executions)
        snapshot = assertion.io.get_snapshot_name(executions)
        self.add_visited_snapshots({filepath: {snapshot}})

        if filepath not in self._assertions:
            self._assertions[filepath] = dict()
        self._assertions[filepath][snapshot] = assertion

    def add_discovered_snapshots(self, albums: Albums):
        self._merge_albums(self.discovered_albums, albums)

    def add_visited_snapshots(self, albums: Albums):
        self._merge_albums(self.visited_albums, albums)

    def remove_unused_snapshots(self):
        for snapshot_file, snapshots in self.unused_snapshots.items():
            # All discovered snapshots in the file are unused
            if self.discovered_albums[snapshot_file] == snapshots:
                os.remove(snapshot_file)
                continue
            # The snapshot file should have at least one registered assertion
            snapshot_file_assertion, *_ = self._assertions[snapshot_file].values()
            for snapshot_name in snapshots:
                snapshot_file_assertion.io.delete_snapshot(snapshot_file, snapshot_name)

    def _merge_albums(self, *albums_to_merge: Albums):
        """
        Add snapshots from other albums into the first one
        """
        merged_albums = albums_to_merge[0]
        for albums in albums_to_merge[1:]:
            for filepath, snapshots in albums.items():
                if self._in_snapshot_dir(filepath):
                    if filepath not in merged_albums:
                        merged_albums[filepath] = set()
                    merged_albums[filepath].update(snapshots)

    def _subtract_albums(self, album1: Albums, album2: Albums) -> Albums:
        diff_albums = dict()
        for filename, snapshots1 in album1.items():
            snapshots2 = album2.get(filename)
            if snapshots2 is None:
                diff_albums[filename] = snapshots1
            else:
                result = snapshots1 - snapshots2
                if result:
                    diff_albums[filename] = result
        return diff_albums

    def _count_snapshots(self, albums: Albums) -> int:
        count = 0
        for _, snapshots in albums.items():
            count += max(1, len(snapshots))
        return count

    def _in_snapshot_dir(self, path: str) -> bool:
        parts = path.split(os.path.sep)
        return SNAPSHOT_DIRNAME in parts

    def _walk_dir(self, root: str):
        for (dirpath, _, filenames) in os.walk(root):
            if not self._in_snapshot_dir(dirpath):
                continue
            for filename in filenames:
                if not filename.startswith("."):
                    yield os.path.join(dirpath, filename)
