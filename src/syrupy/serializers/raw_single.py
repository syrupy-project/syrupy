import os
import re
from gettext import gettext
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Set,
)

from syrupy.data import (
    Snapshot,
    SnapshotFile,
)

from .base import AbstractSnapshotSerializer


if TYPE_CHECKING:
    from syrupy.types import SerializableData, SerializedData  # noqa: F401


class RawSingleSnapshotSerializer(AbstractSnapshotSerializer):
    @property
    def file_extension(self) -> str:
        return "raw"

    def discover_snapshots(self, filepath: str) -> "SnapshotFile":
        """Parse the snapshot name from the filename."""
        snapshot_file = SnapshotFile(filepath=filepath)
        snapshot_file.add(
            Snapshot(name=os.path.splitext(os.path.basename(filepath))[0])
        )
        return snapshot_file

    def get_file_basename(self, index: int) -> str:
        return self.get_snapshot_name(index=index)

    def get_snapshot_name(self, index: int = 0) -> str:
        return self.__clean_filename(
            super(RawSingleSnapshotSerializer, self).get_snapshot_name(index=index)
        )

    @property
    def snapshot_subdirectory_name(self) -> str:
        return os.path.splitext(os.path.basename(str(self.test_location.filename)))[0]

    def _read_snapshot_from_file(
        self, snapshot_filepath: str, snapshot_name: str
    ) -> Optional["SerializableData"]:
        return self._read_file(snapshot_filepath)

    def serialize(self, data: "SerializableData") -> bytes:
        return bytes(data)

    def _read_file(self, filepath: str) -> Any:
        try:
            with open(filepath, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def _write_snapshot_to_file(self, snapshot_file: "SnapshotFile") -> None:
        self.__write_file(snapshot_file.filepath, next(iter(snapshot_file)).data)

    def delete_snapshots_from_file(self, snapshot_filepath: str, _: Set[str]) -> None:
        os.remove(snapshot_filepath)

    def __write_file(self, filepath: str, data: Optional["SerializedData"]) -> None:
        if not isinstance(data, bytes):
            error_text = gettext("Can write non binary data. Expected '{}', got '{}'")
            raise TypeError(error_text.format(bytes.__name__, type(data).__name__))
        with open(filepath, "wb") as f:
            f.write(data)

    def __clean_filename(self, filename: str) -> str:
        filename = str(filename).strip().replace(" ", "_")
        max_filename_length = 255 - len(self.file_extension or "")
        return re.sub(r"(?u)[^-\w.]", "", filename)[:max_filename_length]
