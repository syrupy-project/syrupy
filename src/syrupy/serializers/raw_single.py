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
        return self.__clean_filename(self.get_snapshot_name(index=index))

    @property
    def snapshot_subdirectory_name(self) -> str:
        return os.path.splitext(os.path.basename(str(self.test_location.filename)))[0]

    def _read_snapshot_from_file(
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

    def _write_snapshot_to_file(
        self, snapshot_file: str, snapshot_name: str, data: "SerializableData"
    ) -> None:
        self.__write_file(snapshot_file, data)

    def delete_snapshots_from_file(self, snapshot_file: str, _: Set[str]) -> None:
        os.remove(snapshot_file)

    def __write_file(self, filepath: str, data: "SerializableData") -> None:
        with open(filepath, "wb") as f:
            f.write(self.serialize(data))

    def __clean_filename(self, filename: str) -> str:
        filename = str(filename).strip().replace(" ", "_")
        max_filename_length = 255 - len(self.file_extension or "")
        return re.sub(r"(?u)[^-\w.]", "", filename)[:max_filename_length]
