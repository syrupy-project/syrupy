# type: ignore

# One snapshot file per parametrization — the worst case for unused detection at
# session finish (see syrupy-project/syrupy#1193). A quarter of items run so
# collected ⊃ selected and ~75% of on-disk snapshots are unused.
SNAPSHOT_COUNT = 400
SELECTED_FRACTION = 4

PARTIAL_SELECTION_CONFTEST = f"""
import pytest
from syrupy.extensions.single_file import SingleFileSnapshotExtension


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(SingleFileSnapshotExtension)


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    keep = len(items) // {SELECTED_FRACTION}
    deselected = items[keep:]
    if deselected:
        config.hook.pytest_deselected(items=deselected)
        del items[keep:]
"""

TEST_CONTENTS = f"""
import pytest


@pytest.mark.parametrize("x", range({SNAPSHOT_COUNT}))
def test_performance(x, snapshot):
    assert str(x).encode() == snapshot
"""


def test_partial_selection_teardown(testdir, benchmark):
    """
    Benchmark session finish when collected items outnumber selected items.

    Mirrors shard-like deselection (e.g. pytest-split) with single-file
    snapshots: syrupy records the full collection, but only a subset runs,
    leaving many on-disk snapshot files unused.
    """
    testdir.makeconftest(PARTIAL_SELECTION_CONFTEST)
    testdir.makepyfile(test=TEST_CONTENTS)

    testdir.runpytest("test.py", "--snapshot-update")

    benchmark(lambda: testdir.runpytest("test.py", "--snapshot-warn-unused"))
