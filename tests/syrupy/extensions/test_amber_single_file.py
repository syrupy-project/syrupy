import pytest

from syrupy.extensions.single_file import SingleFileAmberSnapshotExtension


@pytest.fixture
def snapshot_single(snapshot):
    return snapshot.use_extension(SingleFileAmberSnapshotExtension)


def test_amber_single_file(snapshot_single):
    assert snapshot_single == 1
    assert snapshot_single == {"a": "b"}
    assert (
        snapshot_single
        == """
        Multi
        line
        string
    """
    )
