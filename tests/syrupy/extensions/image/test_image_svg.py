import pytest

from syrupy.extensions.image import SVGImageSnapshotExtension

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


@pytest.fixture
def snapshot_svg(snapshot):
    return snapshot.use_extension(SVGImageSnapshotExtension)


def test_image(snapshot_svg):
    assert actual_svg == snapshot_svg


def test_multiple_snapshot_extensions(snapshot):
    """
    Example of switching extension classes on the fly.
    These should be indexed in order of assertion.
    """
    assert actual_svg == snapshot(extension_class=SVGImageSnapshotExtension)
    assert actual_svg == snapshot()  # uses initial extension class
    assert snapshot._extension is not None
    assert actual_svg == snapshot(extension_class=SVGImageSnapshotExtension)
