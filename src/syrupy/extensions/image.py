from typing import (
    TYPE_CHECKING,
    Any,
)

from .single_file import SingleFileSnapshotExtension

if TYPE_CHECKING:
    from syrupy.types import SerializableData


class PNGImageSnapshotExtension(SingleFileSnapshotExtension):
    @property
    def _file_extension(self) -> str:
        return "png"


class SVGImageSnapshotExtension(SingleFileSnapshotExtension):
    @property
    def _file_extension(self) -> str:
        return "svg"

    def serialize(self, data: "SerializableData", **kwargs: Any) -> bytes:
        return str(data).encode("utf-8")
