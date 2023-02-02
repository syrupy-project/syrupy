from typing import (
    TYPE_CHECKING,
    Any,
)

from syrupy.constants import TEXT_ENCODING

from .single_file import SingleFileSnapshotExtension

if TYPE_CHECKING:
    from syrupy.types import SerializableData


class PNGImageSnapshotExtension(SingleFileSnapshotExtension):
    _file_extension = "png"


class SVGImageSnapshotExtension(SingleFileSnapshotExtension):
    _file_extension = "svg"

    def serialize(self, data: "SerializableData", **kwargs: Any) -> bytes:
        return str(data).encode(TEXT_ENCODING)
