import os
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Set,
)

import yaml

from .base import AbstractSnapshotSerializer


if TYPE_CHECKING:
    from syrupy.types import SerializableData


class YAMLSnapshotSerializer(AbstractSnapshotSerializer):
    @property
    def file_extension(self) -> str:
        return "yaml"

    def discover_snapshots(self, filepath: str) -> Set[str]:
        return set(self._read_raw_file(filepath).keys())

    def read_snapshot_from_file(
        self, snapshot_file: str, snapshot_name: str
    ) -> "SerializableData":
        raw_snapshots = self._read_raw_file(snapshot_file)
        return raw_snapshots.get(snapshot_name, None)

    def write_snapshot_or_remove_file(
        self, snapshot_file: str, snapshot_name: str, data: "SerializableData"
    ) -> None:
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
            snapshots[snapshot_name][self._data_key] = data

        if snapshots:
            self._write_file(snapshot_file, snapshots)
        else:
            os.remove(snapshot_file)

    def serialize(self, data: "SerializableData") -> str:
        """
        Returns the serialized form of 'data' to be compared
        with the snapshot data written to disk.
        """
        return str(yaml.dump({self._data_key: data}, allow_unicode=True))

    @property
    def _data_key(self) -> str:
        return "data"

    def _write_file(self, filepath: str, data: "SerializableData") -> None:
        """
        Writes the snapshot data into the snapshot file that be read later.
        """
        with open(filepath, "w") as f:
            yaml.dump(data, f, allow_unicode=True)

    def _read_file(self, filepath: str) -> Any:
        """
        Read the snapshot data from the snapshot file into a python instance.
        """
        try:
            with open(filepath, "r") as f:
                return yaml.load(f, Loader=yaml.FullLoader) or {}
        except FileNotFoundError:
            pass
        return {}

    def _read_raw_file(self, filepath: str) -> Dict[str, str]:
        """
        Read the raw snapshot data (str) from the snapshot file into a dict
        of snapshot name to raw data. This does not attempt any deserialization
        of the snapshot data.
        """
        snapshots = {}
        try:
            with open(filepath, "r") as f:
                test_name = None
                for line in f:
                    indent = len(line) - len(line.lstrip(" "))
                    if not indent:
                        test_name = line[:-2]  # newline & colon
                        snapshots[test_name] = ""
                    elif test_name is not None:
                        snapshots[test_name] += line[2:]
        except FileNotFoundError:
            pass

        return snapshots
