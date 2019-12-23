"""
YAML serializer
"""

import os
from typing import (
    TYPE_CHECKING,
    Any,
    Set,
)

import yaml

from .base import AbstractSnapshotSerializer


if TYPE_CHECKING:
    from syrupy.types import SerializableData


class YAMLSnapshotSerializer(AbstractSnapshotSerializer):
    """
    Implements snapshot seriailizer using PyYAML
    """

    @property
    def file_extension(self) -> str:
        return "yaml"

    def discover_snapshots(self, filepath: str) -> Set[str]:
        try:
            return set(self._read_file(filepath).keys())
        except:  # pylint: disable=bare-except
            return set()

    def read_snapshot_from_file(
        self, snapshot_file: str, snapshot_name: str
    ) -> "SerializableData":
        snapshots = self._read_file(snapshot_file)
        return snapshots.get(snapshot_name, {}).get("data", None)

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
            snapshots[snapshot_name]["data"] = data

        if snapshots:
            self._write_file(snapshot_file, snapshots)
        else:
            os.remove(snapshot_file)

    @staticmethod
    def _write_file(filepath: str, data: "SerializableData") -> None:
        """
        Writes the snapshot data into the snapshot file that be read later.
        """
        with open(filepath, "w") as snap_file:
            yaml.dump(data, snap_file, allow_unicode=True)

    @staticmethod
    def _read_file(filepath: str) -> Any:
        """
        Read the snapshot data from the snapshot file into a python instance.
        """
        try:
            with open(filepath, "r") as snap_file:
                return yaml.load(snap_file, Loader=yaml.FullLoader) or {}
        except FileNotFoundError:
            pass
        return {}
