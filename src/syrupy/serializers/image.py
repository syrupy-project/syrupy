from .raw_single import RawSingleSnapshotSerializer


class PNGImageSnapshotSerializer(RawSingleSnapshotSerializer):
    @property
    def file_extension(self) -> str:
        return "png"


class SVGImageSnapshotSerializer(RawSingleSnapshotSerializer):
    @property
    def file_extension(self) -> str:
        return "svg"
