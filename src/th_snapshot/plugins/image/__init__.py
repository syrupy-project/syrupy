from .io import AbstractImageSnapshotIO
from .serializer import ImageSnapshotSerializer

class PNGImageSnapshotIO(AbstractImageSnapshotIO):
    extension = 'png'

class SVGImageSnapshotIO(AbstractImageSnapshotIO):
    extension = 'svg'
