"""Regression tests for ``--last-failed`` combined with ``--snapshot-update``.

See https://github.com/syrupy-project/syrupy/issues/1251: ``--lf`` skips files
without failures at collection time, so their snapshots must not be treated as
unused and deleted.
"""

from pathlib import Path

import pytest


@pytest.fixture
def testfile(testdir):
    testdir.makepyfile(
        test_foo='def test_foo(snapshot):\n    assert snapshot == "foo"\n',
        test_bar='def test_bar(snapshot):\n    assert snapshot == "bar"\n',
    )
    result = testdir.runpytest("--snapshot-update")
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    testdir.makepyfile(
        test_foo='def test_foo(snapshot):\n    assert snapshot == "zoom"\n'
    )
    result = testdir.runpytest()
    assert result.ret == 1
    return testdir


def test_last_failed_update_keeps_other_snapshots(testfile):
    result = testfile.runpytest("--lf", "--snapshot-update")
    output = result.stdout.str()
    assert "1 snapshot updated" in output
    assert "Deleted" not in output
    assert "unused" not in output

    snapshots = Path(testfile.tmpdir, "__snapshots__")
    assert (snapshots / "test_bar.ambr").exists()
    assert "zoom" in (snapshots / "test_foo.ambr").read_text()
