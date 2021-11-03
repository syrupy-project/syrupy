import base64

import pytest

from syrupy.extensions.image import PNGImageSnapshotExtension


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(PNGImageSnapshotExtension)


def test_png_image_with_custom_name_suffix(snapshot):
    reddish_square = base64.b64decode(
        b"iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAIAAAAmkwkpAAAAIUlEQVQIHTXB"
        b"MQEAAAABQUYtvpD+dUzu3KBzg84NOjfoBjmmAd3WpSsrAAAAAElFTkSuQmCC"
    )

    blueish_square = base64.b64decode(
        b"iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAIAAAAmkwkpAAAAIUlEQVQIHTXB"
        b"MQEAAAABQUYtvpD+dUzuTKozqc6kOpPqBjg+Ad2g/BLMAAAAAElFTkSuQmCC"
    )

    assert blueish_square == snapshot(name="blueish")
    assert reddish_square == snapshot(name="reddish")
