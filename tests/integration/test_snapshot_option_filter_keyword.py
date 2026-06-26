"""Regression tests for snapshot selection with the pytest ``-k`` filter.

See https://github.com/syrupy-project/syrupy/issues/770: a negated keyword
expression such as ``-k 'not one'`` deselects the matching test, and its
snapshot must not be reported (or deleted) as obsolete.
"""

from pathlib import Path

import pytest

CONTENT = """
import pytest

@pytest.mark.parametrize("param", ["one", "two", "three"])
def test_parametrized(param, snapshot):
    assert param == snapshot
"""


@pytest.fixture
def testfile(testdir):
    testdir.makepyfile(test_file=CONTENT)
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"3 snapshots generated\.",))
    return testdir


def test_positive_keyword_filter(testfile):
    result = testfile.runpytest("-v", "-k", "one")
    result.stdout.re_match_lines((r"1 snapshot passed\.",))
    assert "snapshot unused" not in result.stdout.str()


def test_negated_keyword_filter(testfile):
    result = testfile.runpytest("-v", "-k", "not one")
    result.stdout.re_match_lines((r"2 snapshots passed\.",))
    assert "snapshot unused" not in result.stdout.str()


def test_negated_keyword_filter_update_keeps_snapshot(testfile):
    result = testfile.runpytest("-v", "--snapshot-update", "-k", "not one")
    assert "Deleted" not in result.stdout.str()

    snapshot_file = Path(testfile.tmpdir, "__snapshots__", "test_file.ambr")
    assert "test_parametrized[one]" in snapshot_file.read_text()
