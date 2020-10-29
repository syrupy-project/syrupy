import base64

import pytest

from syrupy.extensions.image import PNGImageSnapshotExtension

actual_png = base64.b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAADIAAAAyBAMAAADsEZWCAAAAG1BMVEXMzMy"
    b"Wlpaqqqq3t7exsbGcnJy+vr6jo6PFxcUFpPI/AAAACXBIWXMAAA7EAAAOxA"
    b"GVKw4bAAAAQUlEQVQ4jWNgGAWjgP6ASdncAEaiAhaGiACmFhCJLsMaIiDAE"
    b"QEi0WXYEiMCOCJAJIY9KuYGTC0gknpuHwXDGwAA5fsIZw0iYWYAAAAASUVO"
    b"RK5CYII="
)


@pytest.fixture
def snapshot_png(snapshot):
    return snapshot.use_extension(PNGImageSnapshotExtension)


def test_image(snapshot_png):
    assert actual_png == snapshot_png


def test_multiple_snapshot_extensions(snapshot):
    """
    Example of switching extension classes on the fly.
    These should be indexed in order of assertion.
    """
    assert actual_png == snapshot(extension_class=PNGImageSnapshotExtension)
    assert actual_png == snapshot()  # uses initial extension class
    assert snapshot._extension is not None
    assert actual_png == snapshot(extension_class=PNGImageSnapshotExtension)
