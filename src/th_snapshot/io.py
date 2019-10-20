import os
import yaml

from .exceptions import SnapshotDoesNotExist


class SnapshotIO:
    _test_filename = None
    _test_modulename = None
    _test_classname = None
    _test_methodname = None
    _test_nodename = None

    def __init__(self, **kwargs):
        self._test_filename = kwargs.get("test_filename")
        self._test_modulename = kwargs.get("test_modulename")
        self._test_classname = kwargs.get("test_classname")
        self._test_methodname = kwargs.get("test_methodname")
        self._test_nodename = kwargs.get("test_nodename")

    def write(self, data, index=0):
        self._ensure_dir()
        snapshot_name = self.get_snapshot_name(index)
        snapshots = self._load_documents()
        snapshots[snapshot_name] = snapshots.get(snapshot_name, {})
        snapshots[snapshot_name]["data"] = data
        with open(self.get_filepath(), "w") as f:
            yaml.safe_dump(snapshots, f)

    def read(self, index=0):
        snapshot_name = self.get_snapshot_name(index)
        snapshots = self._load_documents()
        snapshot = snapshots.get(snapshot_name, None)
        if snapshot is None:
            raise SnapshotDoesNotExist()
        return snapshot["data"]

    def get_snapshot_name(self, index=0):
        index_suffix = f".{index}" if index > 0 else ""
        methodname = self._test_nodename or self._test_methodname

        if self._test_classname is not None:
            return f"{self._test_classname}.{methodname}{index_suffix}"
        return f"{methodname}{index_suffix}"

    def get_snapshot_dirname(self):
        return "_snapshots_"

    def get_filepath(self):
        basename = self.get_file_basename()
        return os.path.join(self._get_dirname(), basename)

    def get_file_basename(self):
        return f"{os.path.basename(self._test_filename)[: -len('.py')]}.yaml"

    def _load_documents(self):
        try:
            with open(self.get_filepath(), "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            pass
        return {}

    def _get_dirname(self):
        test_dirname = os.path.dirname(self._test_filename)
        return os.path.join(test_dirname, self.get_snapshot_dirname())

    def _ensure_dir(self):
        try:
            os.makedirs(self._get_dirname())
        except FileExistsError:
            pass
