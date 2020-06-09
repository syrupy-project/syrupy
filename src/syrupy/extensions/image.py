from typing import (
    TYPE_CHECKING,
    Optional,
)

from .single_file import SingleFileSnapshotExtension


if TYPE_CHECKING:
    from syrupy.types import PropertyMatcher, SerializableData


class PNGImageSnapshotExtension(SingleFileSnapshotExtension):
    @property
    def _file_extension(self) -> str:
        return "png"


class SVGImageSnapshotExtension(SingleFileSnapshotExtension):
    @property
    def _file_extension(self) -> str:
        return "svg"

    def serialize(
        self, data: "SerializableData", *, matcher: Optional["PropertyMatcher"] = None,
    ) -> bytes:
        return str(data).encode("utf-8")
