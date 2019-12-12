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


def test_unused_snapshots(testdir):
    pyfile_used_snapshot = """
def test_used(snapshot):
    assert snapshot == 'this snapshot is used'
"""
    pyfile_content = f"""{pyfile_used_snapshot}
def test_unused(snapshot):
    assert snapshot == 'this snapshot will be unused'
"""
    testdir.makepyfile(test_file=pyfile_content)
    result = testdir.runpytest("-v", "--snapshot-update")
    assert "2\x1b[0m snapshots generated" in result.stdout.str()
    assert "0\x1b[0m snapshots unused" in result.stdout.str()
    assert result.ret == 0

    testdir.makepyfile(test_file=pyfile_used_snapshot)
    result = testdir.runpytest("-v")
    assert "snapshots generated" not in result.stdout.str()
    assert "1\x1b[0m snapshot unused" in result.stdout.str()
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
