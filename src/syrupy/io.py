from typing import Any, Callable, Optional, Set

import os
import yaml

from .constants import SNAPSHOT_DIRNAME
from .exceptions import SnapshotDoesNotExist
from .location import TestLocation
from .types import SnapshotFiles


class SnapshotIO:
    def __init__(self, test_location: TestLocation, file_hook):
        self._test_location = test_location
        self._file_hook = file_hook

    @property
    def test_location(self):
        return self._test_location

    @property
    def dirname(self) -> str:
        test_dirname = os.path.dirname(self.test_location.filename)
        snapshot_dir = self._get_snapshot_dirname()
        if snapshot_dir is not None:
            return os.path.join(test_dirname, SNAPSHOT_DIRNAME, snapshot_dir)
        return os.path.join(test_dirname, SNAPSHOT_DIRNAME)

    def discover_snapshots(self, filepath: str) -> Set[str]:
        """
        Utility method for getting all the snapshots from a file.
        Returns an empty set if the file cannot be read.
        """
        try:
            return set(self._read_file(filepath).keys())
        except:
            return set()

    def read_snapshot(self, index: int) -> Any:
        """
        Utility method for reading the contents of a snapshot assertion.
        Will call `pre_read`, then `read` and finally `post_read`,
        returning the contents parsed from the `read` method.
        """
        try:
            self.pre_read(index=index)
            return self.read(index=index)
        finally:
            self.post_read(index=index)

    def create_or_update_snapshot(self, serialized_data: Any, index: int):
        """
        Utility method for reading the contents of a snapshot assertion.
        Will call `pre_write`, then `write` and finally `post_write`.
        """
        self.pre_write(serialized_data, index=index)
        self.write(serialized_data, index=index)
        self.post_write(serialized_data, index=index)

    def delete_snapshot(self, snapshot_file: str, snapshot_name: str):
        """
        Utility method for removing a snapshot from a snapshot file.
        """
        self._write_snapshot_or_remove_file(snapshot_file, snapshot_name, None)

    def pre_read(self, index: int = 0):
        pass

    def read(self, index: int = 0) -> Any:
        snapshot_file = self.get_filepath(index)
        snapshot_name = self.get_snapshot_name(index)
        snapshot = self._read_snapshot_from_file(snapshot_file, snapshot_name)
        if snapshot is None:
            raise SnapshotDoesNotExist()
        return snapshot

    def post_read(self, index: int = 0):
        self._snap_file_hook(index)

    def pre_write(self, data: Any, index: int = 0):
        self._ensure_snapshot_dir(index)

    def write(self, data: Any, index: int = 0):
        snapshot_file = self.get_filepath(index)
        snapshot_name = self.get_snapshot_name(index)
        self._write_snapshot_or_remove_file(snapshot_file, snapshot_name, data)

    def post_write(self, data: Any, index: int = 0):
        self._snap_file_hook(index)

    def get_snapshot_name(self, index: int = 0) -> str:
        index_suffix = f".{index}" if index > 0 else ""
        methodname = self._test_location.testname

        if self._test_location.classname is not None:
            return f"{self._test_location.classname}.{methodname}{index_suffix}"
        return f"{methodname}{index_suffix}"

    def get_filepath(self, index: int) -> str:
        basename = self.get_file_basename(index=index)
        return os.path.join(self.dirname, basename)

    def get_file_basename(self, index: int) -> str:
        return f"{os.path.splitext(os.path.basename(self._test_location.filename))[0]}.yaml"

    def _get_snapshot_dirname(self) -> Optional[str]:
        return None

    def _ensure_snapshot_dir(self, index: int):
        """
        Ensures the folder path for the snapshot file exists.
        """
        try:
            os.makedirs(os.path.dirname(self.get_filepath(index)))
        except FileExistsError:
            pass

    def _read_snapshot_from_file(self, snapshot_file: str, snapshot_name: str) -> Any:
        """
        Read the snapshot file and get only the snapshot data for assertion
        """
        snapshots = self._read_file(snapshot_file)
        return snapshots.get(snapshot_name, {}).get("data", None)

    def _read_file(self, filepath: str) -> Any:
        """
        Read the snapshot data from the snapshot file into a python instance.
        """
        try:
            with open(filepath, "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            pass
        return {}

    def _write_snapshot_or_remove_file(
        self, snapshot_file: str, snapshot_name: str, data: Any
    ):
        """
        Adds the snapshot data to the snapshots read from the file
        or removes the snapshot entry if data is `None`.
        If the snapshot file will be empty remove the entire file.
        """
        snapshots = self._read_file(snapshot_file)
        if data is None and snapshot_name in snapshots:
            del snapshots[snapshot_name]
        else:
            snapshots[snapshot_name] = snapshots.get(snapshot_name, {})
            snapshots[snapshot_name]["data"] = data

        if snapshots:
            self._write_file(snapshot_file, snapshots)
        else:
            os.remove(snapshot_file)

    def _write_file(self, filepath: str, data: Any):
        """
        Writes the snapshot data into the snapshot file that be read later.
        """
        with open(filepath, "w") as f:
            yaml.safe_dump(data, f)

    def _snap_file_hook(self, index: int):
        """
        Notify the assertion of an access to a snapshot in a file
        """
        snapshot_file = self.get_filepath(index)
        snapshot_name = self.get_snapshot_name(index)
        self._file_hook(snapshot_file, snapshot_name)
