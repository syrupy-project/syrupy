import os
import re

import pytest


@pytest.fixture
def testcases():
    return {
        "inject": (
            """
            def test_injection(snapshot):
                assert snapshot is not None
            """
        ),
        "used": (
            """
            def test_used(snapshot):
                assert snapshot == 'used'
            """
        ),
        "unused": (
            """
            def test_unused(snapshot):
                assert snapshot == 'unused'
            """
        ),
    }


def test_missing_snapshots(testdir, testcases):
    testdir.makepyfile(test_file=testcases["used"])
    result = testdir.runpytest("-v")
    assert "Snapshot does not exist" in _clean_output(result.stdout.str())
    assert result.ret == 1


@pytest.fixture
def stubs(testdir, testcases):
    pyfile_content = "\n\n".join(testcases.values())
    testdir.makepyfile(test_file=pyfile_content)
    filepath = os.path.join(testdir.tmpdir, "__snapshots__", "test_file.yaml")
    return testdir.runpytest("-v", "--snapshot-update"), testdir, testcases, filepath


def test_injected_fixture(stubs):
    result = stubs[0]
    result.stdout.fnmatch_lines(["*::test_injection PASSED*"])
    assert result.ret == 0


def test_generated_snapshots(stubs):
    result = stubs[0]
    result_stdout = _clean_output(result.stdout.str())
    assert "2 snapshots generated" in result_stdout
    assert "snapshots unused" not in result_stdout
    assert result.ret == 0


def test_unused_snapshots(stubs):
    result, testdir, tests, _ = stubs
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v")
    result_stdout = _clean_output(result.stdout.str())
    assert "snapshots generated" not in result_stdout
    assert "1 snapshot passed" in result_stdout
    assert "1 snapshot unused" in result_stdout
    assert result.ret == 0


def test_removed_snapshots(stubs):
    _, testdir, tests, filepath = stubs
    assert os.path.isfile(filepath)
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = _clean_output(result.stdout.str())
    assert "snapshot unused" not in result_stdout
    assert "1 snapshot deleted" in result_stdout
    assert result.ret == 0
    assert os.path.isfile(filepath)


def test_removed_snapshot_file(stubs):
    _, testdir, tests, filepath = stubs
    assert os.path.isfile(filepath)
    testdir.makepyfile(test_file=tests["inject"])
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = _clean_output(result.stdout.str())
    assert "snapshots unused" not in result_stdout
    assert "2 snapshots deleted" in result_stdout
    assert result.ret == 0
    assert not os.path.isfile(filepath)


def _clean_output(output: str) -> str:
    """Removes ansi color codes from string"""
    return re.sub(r"\x1B[@-_][0-?]*[ -/]*[@-~]", "", str(output).strip())
