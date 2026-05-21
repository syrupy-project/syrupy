import sys
from pathlib import Path

import pytest


@pytest.fixture
def testcases_initial():
    return {
        "test_one": (
            """
            def test_one(snapshot):
                assert snapshot == 'first'
            """
        ),
    }


@pytest.fixture
def testcases_with_new(testcases_initial):
    updates = {
        "test_one": (
            """
            def test_one(snapshot):
                assert snapshot == 'first'

            def test_two(snapshot):
                assert snapshot == 'second'
            """
        ),
    }
    return {**testcases_initial, **updates}


@pytest.fixture
def testcases_with_change(testcases_initial):
    updates = {
        "test_one": (
            """
            def test_one(snapshot):
                assert snapshot == 'changed'
            """
        ),
    }
    return {**testcases_initial, **updates}


@pytest.fixture
def run_testcases(testdir, testcases_initial):
    sys.path.append(str(testdir.tmpdir))
    testdir.makepyfile(**testcases_initial)
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"1 snapshot generated\.",))
    return result, testdir, testcases_initial


def test_update_new_only_creates_missing_snapshot(run_testcases, testcases_with_new):
    testdir = run_testcases[1]
    testdir.makepyfile(**testcases_with_new)
    result = testdir.runpytest("-v", "--snapshot-update-new-only")
    result.stdout.re_match_lines((r"1 snapshot passed\. 1 snapshot generated\.",))
    assert "1 snapshot updated" not in result.stdout.str()
    assert result.ret == 0
    snapshot_file = Path(testdir.tmpdir, "__snapshots__", "test_one.ambr")
    assert snapshot_file.exists()
    contents = snapshot_file.read_text()
    assert "first" in contents
    assert "second" in contents


def test_update_new_only_does_not_modify_existing_snapshot(
    run_testcases, testcases_with_change
):
    testdir = run_testcases[1]
    testdir.makepyfile(**testcases_with_change)
    result = testdir.runpytest("-v", "--snapshot-update-new-only")
    assert "1 snapshot generated" not in result.stdout.str()
    assert "1 snapshot updated" not in result.stdout.str()
    assert result.ret != 0
    snapshot_file = Path(testdir.tmpdir, "__snapshots__", "test_one.ambr")
    assert snapshot_file.exists()
    contents = snapshot_file.read_text()
    assert "first" in contents
    assert "changed" not in contents


def test_default_still_fails_on_missing_snapshot(run_testcases, testcases_with_new):
    testdir = run_testcases[1]
    testdir.makepyfile(**testcases_with_new)
    result = testdir.runpytest("-v")
    assert "1 snapshot generated" not in result.stdout.str()
    assert "1 snapshot updated" not in result.stdout.str()
    assert result.ret != 0
    snapshot_file = Path(testdir.tmpdir, "__snapshots__", "test_one.ambr")
    assert snapshot_file.exists()
    contents = snapshot_file.read_text()
    assert "second" not in contents
