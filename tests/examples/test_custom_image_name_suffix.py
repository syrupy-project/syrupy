from syrupy.extensions.image import PNGImageSnapshotExtension
import base64
import pytest


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

    assert blueish_square == snapshot(snapshot_name_suffix="blueish")
    assert reddish_square == snapshot(snapshot_name_suffix="reddish")
