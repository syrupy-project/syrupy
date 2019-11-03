import os

from .constants import SNAPSHOT_DIRNAME

class SnapshotSession:
    def __init__(self, *, update_snapshots: bool, base_dir: str):
        self.update_snapshots = update_snapshots
        self.base_dir = base_dir
        self.discovered_snapshots = None
        self.visited_snapshots = None
        self.report = []

    def start(self):
        self.report = []
        self.visited_snapshots = set()
        self.discovered_snapshots = set(
            filepath for filepath in self._walk_dir(self.base_dir)
        )

    def add_visited_file(self, filepath):
        dirname = os.path.dirname(filepath)
        if os.path.basename(dirname) == SNAPSHOT_DIRNAME:
            self.visited_snapshots.add(filepath)

    def add_report_line(self, line: str = ""):
        self.report += [line]

    def finish(self):
        unused_snapshots = self.discovered_snapshots - self.visited_snapshots
        self.add_report_line()
        self.add_report_line(f"There are {len(unused_snapshots)} snapshot files unused.")
        for filepath in unused_snapshots:
            self.add_report_line(f"  {filepath}")
        self.add_report_line()


    def _walk_dir(self, root: str):
        for (dirpath, dirnames, filenames) in os.walk(root):
            dirname = os.path.basename(dirpath)
            if dirname != SNAPSHOT_DIRNAME:
                continue
            dirnames[:] = []
            for filename in filenames:
                if not filename.startswith("."):
                    yield os.path.join(dirpath, filename)
