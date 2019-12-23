"""
Snapshot serializer image plugins
"""
from .raw_single import RawSingleSnapshotSerializer


class PNGImageSnapshotSerializer(RawSingleSnapshotSerializer):
    """
    Implement raw single snapshot serializer into PNG file
    """

    @property
    def file_extension(self) -> str:
        return "png"


class SVGImageSnapshotSerializer(RawSingleSnapshotSerializer):
    """
    Implement raw single snapshot serializer into SVG file
    """

    @property
    def file_extension(self) -> str:
        return "svg"
