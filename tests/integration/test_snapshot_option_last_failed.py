"""Regression tests for ``--last-failed`` combined with ``--snapshot-update``.

See https://github.com/syrupy-project/syrupy/issues/1251: ``--lf`` skips files
without failures at collection time, so their snapshots must not be treated as
unused and deleted. A run with no cached failures still executes the suite and
must keep deleting obsolete snapshots.
"""

from pathlib import Path

import pytest


def _snapshots(testdir) -> Path:
    return Path(testdir.tmpdir, "__snapshots__")


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
    assert result.ret == 0
    assert "1 snapshot updated" in output
    assert "Deleted" not in output
    assert "unused" not in output

    snapshots = _snapshots(testfile)
    assert "bar" in (snapshots / "test_bar.ambr").read_text()
    assert "zoom" in (snapshots / "test_foo.ambr").read_text()


def test_last_failed_update_keeps_sibling_in_same_file(testdir):
    testdir.makepyfile(
        test_foo=(
            "def test_a(snapshot):\n"
            '    assert snapshot == "a"\n'
            "\n"
            "def test_b(snapshot):\n"
            '    assert snapshot == "b"\n'
        )
    )
    result = testdir.runpytest("--snapshot-update")
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    testdir.makepyfile(
        test_foo=(
            "def test_a(snapshot):\n"
            '    assert snapshot == "zoom"\n'
            "\n"
            "def test_b(snapshot):\n"
            '    assert snapshot == "b"\n'
        )
    )
    result = testdir.runpytest()
    assert result.ret == 1

    result = testdir.runpytest("--lf", "--snapshot-update")
    output = result.stdout.str()
    assert result.ret == 0
    assert "1 snapshot updated" in output
    assert "Deleted" not in output
    assert "unused" not in output

    snapshot = (_snapshots(testdir) / "test_foo.ambr").read_text()
    assert "zoom" in snapshot
    assert "b" in snapshot


def test_last_failed_without_failures_deletes_obsolete_snapshots(testdir):
    testdir.makepyfile(
        test_foo='def test_foo(snapshot):\n    assert snapshot == "foo"\n',
        test_bar='def test_bar(snapshot):\n    assert snapshot == "bar"\n',
    )
    result = testdir.runpytest("--snapshot-update")
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    assert result.ret == 0

    Path(testdir.tmpdir, "test_bar.py").unlink()
    result = testdir.runpytest("--lf", "--snapshot-update")
    result.stdout.re_match_lines((r"1 snapshot passed\. 1 unused snapshot deleted\.",))
    assert result.ret == 0

    snapshots = _snapshots(testdir)
    assert not (snapshots / "test_bar.ambr").exists()
    assert "foo" in (snapshots / "test_foo.ambr").read_text()
