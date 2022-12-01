from enum import Enum
from gettext import gettext
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Optional,
    Set,
    Type,
    Union,
)
from unicodedata import category

from syrupy.constants import TEXT_ENCODING
from syrupy.data import (
    Snapshot,
    SnapshotCollection,
)
from syrupy.location import PyTestLocation

from .base import AbstractSyrupyExtension

if TYPE_CHECKING:
    from syrupy.types import (
        PropertyFilter,
        PropertyMatcher,
        SerializableData,
        SerializedData,
        SnapshotIndex,
    )


class WriteMode(Enum):
    BINARY = "b"
    TEXT = "t"

    def __str__(self) -> str:
        return self.value


class SingleFileSnapshotExtension(AbstractSyrupyExtension):
    _text_encoding = TEXT_ENCODING
    _write_mode = WriteMode.BINARY
    _file_extension = "raw"

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> "SerializedData":
        return self._supported_dataclass(data)

    @classmethod
    def get_snapshot_name(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex" = 0
    ) -> str:
        return cls.__clean_filename(
            AbstractSyrupyExtension.get_snapshot_name(
                test_location=test_location, index=index
            )
        )

    def delete_snapshots(
        self, *, snapshot_location: str, snapshot_names: Set[str]
    ) -> None:
        Path(snapshot_location).unlink()

    def _get_file_basename(self, *, index: "SnapshotIndex") -> str:
        return self.get_snapshot_name(test_location=self.test_location, index=index)

    @property
    def _dirname(self) -> str:
        original_dirname = super(SingleFileSnapshotExtension, self)._dirname
        return str(Path(original_dirname).joinpath(self.test_location.basename))

    def _read_snapshot_collection(
        self, *, snapshot_location: str
    ) -> "SnapshotCollection":
        snapshot_collection = SnapshotCollection(location=snapshot_location)
        snapshot_collection.add(Snapshot(name=Path(snapshot_location).stem))
        return snapshot_collection

    def _read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str, session_id: str
    ) -> Optional["SerializableData"]:
        try:
            with open(
                snapshot_location, f"r{self._write_mode}", encoding=self._write_encoding
            ) as f:
                return f.read()
        except FileNotFoundError:
            return None

    @property
    def _supported_dataclass(self) -> Union[Type[str], Type[bytes]]:
        if self._write_mode == WriteMode.TEXT:
            return str
        return bytes

    @property
    def _write_encoding(self) -> Optional[str]:
        if self._write_mode == WriteMode.TEXT:
            return TEXT_ENCODING
        return None

    def _write_snapshot_collection(
        self, *, snapshot_collection: "SnapshotCollection"
    ) -> None:
        filepath, data = (
            snapshot_collection.location,
            next(iter(snapshot_collection)).data,
        )
        if not isinstance(data, self._supported_dataclass):
            error_text = gettext(
                "Can't write non supported data. Expected '{}', got '{}'"
            )
            raise TypeError(
                error_text.format(
                    self._supported_dataclass.__name__, type(data).__name__
                )
            )
        with open(filepath, f"w{self._write_mode}", encoding=self._write_encoding) as f:
            f.write(data)

    @classmethod
    def __clean_filename(cls, filename: str) -> str:
        max_filename_length = 255 - len(cls._file_extension or "")
        exclude_chars = '\\/?*:|"<>'
        exclude_categ = ("C",)
        cleaned_filename = "".join(
            c
            for c in filename
            if c not in exclude_chars
            and not any(categ in category(c) for categ in exclude_categ)
        )
        return cleaned_filename[:max_filename_length]
