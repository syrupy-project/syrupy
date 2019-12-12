import pytest


def test_fixture(testdir):
    pyfile_content = """
def test_sth(snapshot):
    assert snapshot is not None
"""
    testdir.makepyfile(pyfile_content)

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_sth PASSED*"])

    assert result.ret == 0


@pytest.fixture
def snapshot_atomic(snapshot):
    previous_count = snapshot.num_executions
    previous_update_snapshots = snapshot._update_snapshots
    snapshot._update_snapshots = True
    yield snapshot
    for i in range(previous_count, snapshot.num_executions):
        snapshot.serializer.write(None, i)
    snapshot._update_snapshots = previous_update_snapshots
    snapshot._executions = previous_count


def test_written_snapshots(snapshot_atomic):
    snapshot_data = "This snapshot should not be committed"
    assert snapshot_data == snapshot_atomic
    snapshot_file = snapshot_atomic.serializer.get_filepath(
        snapshot_atomic.num_executions
    )
    with open(snapshot_file, "r") as f:
        assert snapshot_data in f.read()
