import os
import re
from typing import (
    TYPE_CHECKING,
    Any,
    Set,
)

from .base import AbstractSnapshotSerializer


if TYPE_CHECKING:
    from syrupy.types import SerializableData


class RawSingleSnapshotSerializer(AbstractSnapshotSerializer):
    @property
    def file_extension(self) -> str:
        return "raw"

    def discover_snapshots(self, filepath: str) -> Set[str]:
        """Parse the snapshot name from the filename."""
        return {os.path.splitext(os.path.basename(filepath))[0]}

    def get_file_basename(self, index: int) -> str:
        return self._clean_filename(self.get_snapshot_name(index=index))

    @property
    def snapshot_subdirectory_name(self) -> str:
        return os.path.splitext(os.path.basename(str(self.test_location.filename)))[0]

    def read_snapshot_from_file(
        self, snapshot_file: str, snapshot_name: str
    ) -> "SerializableData":
        return self._read_file(snapshot_file)

    def serialize(self, data: "SerializableData") -> bytes:
        return bytes(data)

    def _read_file(self, filepath: str) -> Any:
        try:
            with open(filepath, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def write_snapshot_or_remove_file(
        self, snapshot_file: str, snapshot_name: str, data: "SerializableData"
    ) -> None:
        if data:
            self._write_file(snapshot_file, data)
        else:
            os.remove(snapshot_file)

    def _write_file(self, filepath: str, data: "SerializableData") -> None:
        with open(filepath, "wb") as f:
            f.write(self.serialize(data))

    def _clean_filename(self, filename: str) -> str:
        filename = str(filename).strip().replace(" ", "_")
        max_filename_length = 255 - len(self.file_extension or "")
        return re.sub(r"(?u)[^-\w.]", "", filename)[:max_filename_length]
