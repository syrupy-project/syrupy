from typing import TYPE_CHECKING

from .raw_single import RawSingleSnapshotSerializer


if TYPE_CHECKING:
    from syrupy.types import SerializableData


class PNGImageSnapshotSerializer(RawSingleSnapshotSerializer):
    @property
    def file_extension(self) -> str:
        return "png"


class SVGImageSnapshotSerializer(RawSingleSnapshotSerializer):
    @property
    def file_extension(self) -> str:
        return "svg"

    def serialize(self, data: "SerializableData") -> bytes:
        return str(data).encode("utf-8")
