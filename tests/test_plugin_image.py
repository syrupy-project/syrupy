import base64

import pytest

from syrupy.serializers.image import (
    PNGImageSnapshotSerializer,
    SVGImageSnapshotSerializer,
)


@pytest.fixture
def snapshot_png(snapshot):
    return snapshot.with_class(serializer_class=PNGImageSnapshotSerializer)


@pytest.fixture
def snapshot_svg(snapshot):
    return snapshot.with_class(serializer_class=SVGImageSnapshotSerializer)


def test_image(snapshot_png, snapshot_svg):
    actual_png = base64.b64decode(
        b"iVBORw0KGgoAAAANSUhEUgAAADIAAAAyBAMAAADsEZWCAAAAG1BMVEXMzMy"
        b"Wlpaqqqq3t7exsbGcnJy+vr6jo6PFxcUFpPI/AAAACXBIWXMAAA7EAAAOxA"
        b"GVKw4bAAAAQUlEQVQ4jWNgGAWjgP6ASdncAEaiAhaGiACmFhCJLsMaIiDAE"
        b"QEi0WXYEiMCOCJAJIY9KuYGTC0gknpuHwXDGwAA5fsIZw0iYWYAAAAASUVO"
        b"RK5CYII="
    )
    assert actual_png == snapshot_png

    actual_svg = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<svg viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">'
        '<g><rect width="50" height="50" fill="#fff"/>'
        '<g><g fill="#fff" stroke="#707070">'
        '<rect width="50" height="50" stroke="none"/>'
        '<rect x="0" y="0" width="50" height="50" fill="none"/></g>'
        '<text transform="translate(10 27)" fill="#707070" '
        'font-family="ConsolasForPowerline, Consolas for Powerline" font-size="8">'
        '<tspan x="0" y="0">50 x 50</tspan></text></g></g></svg>'
    )
    assert snapshot_svg == actual_svg
