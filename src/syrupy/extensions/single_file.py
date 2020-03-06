import re
from gettext import gettext
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Optional,
    Set,
)

from syrupy.data import (
    Snapshot,
    SnapshotFossil,
)

from .base import AbstractSyrupyExtension


if TYPE_CHECKING:
    from syrupy.types import SerializableData, SerializedData  # noqa: F401


class SingleFileSnapshotExtension(AbstractSyrupyExtension):
    def serialize(self, data: "SerializableData") -> bytes:
        return bytes(data)

    def get_snapshot_name(self, *, index: int = 0) -> str:
        return self.__clean_filename(
            super(SingleFileSnapshotExtension, self).get_snapshot_name(index=index)
        )

    def delete_snapshots(
        self, *, snapshot_location: str, snapshot_names: Set[str]
    ) -> None:
        Path(snapshot_location).unlink()

    @property
    def _file_extension(self) -> str:
        return "raw"

    def _get_file_basename(self, *, index: int) -> str:
        return self.get_snapshot_name(index=index)

    @property
    def _dirname(self) -> str:
        original_dirname = super(SingleFileSnapshotExtension, self)._dirname
        return str(Path(original_dirname).joinpath(self.test_location.filename))

    def _read_snapshot_fossil(self, *, snapshot_location: str) -> "SnapshotFossil":
        snapshot_fossil = SnapshotFossil(location=snapshot_location)
        snapshot_fossil.add(Snapshot(name=Path(snapshot_location).stem))
        return snapshot_fossil

    def _read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str
    ) -> Optional["SerializableData"]:
        try:
            with open(snapshot_location, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def _write_snapshot_fossil(self, *, snapshot_fossil: "SnapshotFossil") -> None:
        filepath, data = snapshot_fossil.location, next(iter(snapshot_fossil)).data
        if not isinstance(data, bytes):
            error_text = gettext("Can write non binary data. Expected '{}', got '{}'")
            raise TypeError(error_text.format(bytes.__name__, type(data).__name__))
        with open(filepath, "wb") as f:
            f.write(data)

    def __clean_filename(self, filename: str) -> str:
        filename = str(filename).strip().replace(" ", "_")
        max_filename_length = 255 - len(self._file_extension or "")
        return re.sub(r"(?u)[^-\w.]", "", filename)[:max_filename_length]
