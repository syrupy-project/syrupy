from .io import AbstractImageSnapshotIO
from .serializer import ImageSnapshotSerializer


class PNGImageSnapshotIO(AbstractImageSnapshotIO):
    @property
    def extension(self):
        return "png"


class SVGImageSnapshotIO(AbstractImageSnapshotIO):
    @property
    def extension(self):
        return "svg"
