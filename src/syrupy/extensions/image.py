from typing import TYPE_CHECKING

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

    def serialize(self, data: "SerializableData") -> bytes:
        return str(data).encode("utf-8")
