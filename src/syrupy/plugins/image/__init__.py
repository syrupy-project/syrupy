from .io import AbstractImageSnapshotIO
from .serializer import ImageSnapshotSerializer


class PNGImageSnapshotIO(AbstractImageSnapshotIO):
    @property
    def extension(self) -> str:
        return "png"


class SVGImageSnapshotIO(AbstractImageSnapshotIO):
    @property
    def extension(self) -> str:
        return "svg"
