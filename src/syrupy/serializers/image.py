from typing import TYPE_CHECKING

from .raw_single import RawSingleSnapshotSerializer


if TYPE_CHECKING:
    from syrupy.types import SerializableData


class PNGImageSnapshotSerializer(RawSingleSnapshotSerializer):
    @property
    def file_extension(self) -> str:
        return "png"

    def serialize(self, data: "SerializableData") -> bytes:
        if isinstance(data, bytes):
            return data
        raise TypeError(
            "Can not serialize image data. Expected "
            f"'bytes', got '{type(data).__name__}'."
        )


class SVGImageSnapshotSerializer(RawSingleSnapshotSerializer):
    @property
    def file_extension(self) -> str:
        return "svg"

    def serialize(self, data: "SerializableData") -> bytes:
        return str(data).encode("utf-8")
