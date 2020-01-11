from typing import TYPE_CHECKING

from .raw_single import RawSingleSnapshotExtension


if TYPE_CHECKING:
    from syrupy.types import SerializableData


class PNGImageSnapshotExtension(RawSingleSnapshotExtension):
    @property
    def _file_extension(self) -> str:
        return "png"


class SVGImageSnapshotExtension(RawSingleSnapshotExtension):
    @property
    def _file_extension(self) -> str:
        return "svg"

    def serialize(self, data: "SerializableData") -> bytes:
        return str(data).encode("utf-8")
