"""
Test bundled image plugins
"""

import base64

import pytest

from syrupy.serializers.image import PNGImageSnapshotSerializer


@pytest.fixture(name="snapshot_png")
def fixture_snapshot_png(snapshot):
    """
    PNG snapshot assertion fixture
    """
    return snapshot.with_class(serializer_class=PNGImageSnapshotSerializer)


def test_image(snapshot_png):
    """
    Test snapshot image fixture assertion
    """
    actual = base64.b64decode(
        b"iVBORw0KGgoAAAANSUhEUgAAADIAAAAyBAMAAADsEZWCAAAAG1BMVEXMzMy"
        b"Wlpaqqqq3t7exsbGcnJy+vr6jo6PFxcUFpPI/AAAACXBIWXMAAA7EAAAOxA"
        b"GVKw4bAAAAQUlEQVQ4jWNgGAWjgP6ASdncAEaiAhaGiACmFhCJLsMaIiDAE"
        b"QEi0WXYEiMCOCJAJIY9KuYGTC0gknpuHwXDGwAA5fsIZw0iYWYAAAAASUVO"
        b"RK5CYII="
    )
    assert actual == snapshot_png
