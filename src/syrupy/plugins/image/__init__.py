from .serializer import AbstractImageSnapshotSerializer


class PNGImageSnapshotSerializer(AbstractImageSnapshotSerializer):
    @property
    def extension(self) -> str:
        return "png"


class SVGImageSnapshotSerializer(AbstractImageSnapshotSerializer):
    @property
    def extension(self) -> str:
        return "svg"
