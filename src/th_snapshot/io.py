from typing import Any

import os
import yaml

from .exceptions import SnapshotDoesNotExist
from .location import TestLocation


class SnapshotIO:
    def __init__(self, test_location: TestLocation):
        self._test_location = test_location

    def write(self, data: Any, index: int = 0):
        self.ensure_snapshot_dir(index)
        snapshot_name = self.get_snapshot_name(index)
        snapshots = self._load_documents(index)
        snapshots[snapshot_name] = snapshots.get(snapshot_name, {})
        snapshots[snapshot_name]["data"] = data
        with open(self.get_filepath(index), "w") as f:
            yaml.safe_dump(snapshots, f)

    def read(self, index: int = 0) -> Any:
        snapshot_name = self.get_snapshot_name(index)
        snapshots = self._load_documents(index)
        snapshot = snapshots.get(snapshot_name, None)
        if snapshot is None:
            raise SnapshotDoesNotExist()
        return snapshot["data"]

    def get_snapshot_name(self, index: int = 0) -> str:
        index_suffix = f".{index}" if index > 0 else ""
        methodname = self._test_location.testname

        if self._test_location.classname is not None:
            return f"{self._test_location.classname}.{methodname}{index_suffix}"
        return f"{methodname}{index_suffix}"

    def get_snapshot_dirname(self) -> str:
        return "_snapshots_"

    def get_filepath(self, index: int) -> str:
        basename = self.get_file_basename(index=index)
        return os.path.join(self._get_dirname(), basename)

    def get_file_basename(self, index: int) -> str:
        return f"{os.path.basename(self._test_location.filename)[: -len('.py')]}.yaml"

    def ensure_snapshot_dir(self, index: int):
        try:
            os.makedirs(os.path.dirname(self.get_filepath(index)))
        except FileExistsError:
            pass

    @property
    def test_location(self):
        return self._test_location

    def _load_documents(self, index: int) -> dict:
        try:
            with open(self.get_filepath(index), "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            pass
        return {}

    def _get_dirname(self) -> str:
        test_dirname = os.path.dirname(self._test_location.filename)
        return os.path.join(test_dirname, self.get_snapshot_dirname())
