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


def test_read_snapshot_data_from_missing_file_returns_none(tmp_path):
    ins = SingleFileAmberSnapshotExtension()
    location = tmp_path / "invalid_path.ambr"
    snapshot_data = ins.read_snapshot_data_from_location(
        snapshot_location=str(location),
        snapshot_name="test_name",
        session_id="test_id",
    )
    assert snapshot_data is None


def test_read_snapshot_data_from_empty_file_returns_none(tmp_path):
    ins = SingleFileAmberSnapshotExtension()
    location = tmp_path / "empty_file.ambr"
    location.touch()
    snapshot_data = ins.read_snapshot_data_from_location(
        snapshot_location=str(location),
        snapshot_name="test_name",
        session_id="test_id",
    )
    assert snapshot_data is None
