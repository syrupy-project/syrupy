import os
from gettext import ngettext, gettext
from typing import List, Set

from .constants import SNAPSHOT_DIRNAME
from .terminal import yellow, bold


class SnapshotSession:
    def __init__(self, *, update_snapshots: bool, base_dir: str):
        self.update_snapshots = update_snapshots
        self.base_dir = base_dir
        self.discovered_snapshots: Set[str] = set()
        self.visited_snapshots: Set[str] = set()
        self.report: List[str] = []

    def start(self):
        self.report = []
        self.visited_snapshots = set()
        self.discovered_snapshots = set(
            filepath for filepath in self._walk_dir(self.base_dir)
        )

    @property
    def unused_snapshots(self):
        return self.discovered_snapshots - self.visited_snapshots

    @property
    def written_snapshots(self):
        return self.visited_snapshots - self.discovered_snapshots

    def add_visited_file(self, filepath: str):
        if self._in_snapshot_dir(filepath):
            self.visited_snapshots.add(filepath)

    def add_report_line(self, line: str = ""):
        self.report += [line]

    def finish(self):
        n_unused = len(self.unused_snapshots)
        n_written = len(self.written_snapshots)

        self.add_report_line()

        summary_lines = []
        if self.update_snapshots and n_written:
            summary_lines += [
                ngettext(
                    "{} snapshot file generated.",
                    "{} snapshot files generated.",
                    n_written,
                ).format(bold(n_written))
            ]
        summary_lines += [
            ngettext(
                "{} snapshot file unused.", "{} snapshot files unused.", n_unused
            ).format(bold(n_unused))
        ]
        summary_line = " ".join(summary_lines)
        self.add_report_line(
            yellow(summary_line)
            if n_unused or (self.update_snapshots and n_written)
            else summary_line
        )

        for filepath in self.unused_snapshots:
            self.add_report_line(f"  {os.path.relpath(filepath, self.base_dir)}")

        if n_unused:
            self.add_report_line()
            if self.update_snapshots:
                self.remove_unused_snapshots()
                self.add_report_line(
                    ngettext(
                        "This file has been deleted.",
                        "These files have been deleted.",
                        n_unused,
                    )
                )
            else:
                self.add_report_line(
                    gettext(
                        "Re-run pytest with --update-snapshots to delete these files."
                    )
                )

    def remove_unused_snapshots(self):
        for snapshot_file in self.unused_snapshots:
            os.remove(snapshot_file)

    def _in_snapshot_dir(self, path: str) -> bool:
        parts = path.split(os.path.sep)
        return SNAPSHOT_DIRNAME in parts

    def _walk_dir(self, root: str):
        for (dirpath, dirnames, filenames) in os.walk(root):
            if not self._in_snapshot_dir(dirpath):
                continue
            for filename in filenames:
                if not filename.startswith("."):
                    yield os.path.join(dirpath, filename)
