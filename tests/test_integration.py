import os

import pytest

from .utils import clean_output


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
        "updated_1": (
            """
            def test_updated_1(snapshot):
                assert snapshot == ['this', 'will', 'be', 'updated']
            """
        ),
        "updated_2": (
            """
            def test_updated_2(snapshot):
                assert ['this', 'will', 'be', 'updated'] == snapshot
            """
        ),
        "updated_3": (
            """
            def test_updated_3(snapshot):
                assert snapshot == ['this', 'will', 'be', 'updated']
            """
        ),
    }


@pytest.fixture
def testcases_updated(testcases):
    updated_testcases = {
        "updated_1": (
            """
            def test_updated_1(snapshot):
                assert snapshot == ['this', 'will', 'not', 'match']
            """
        ),
        "updated_2": (
            """
            def test_updated_2(snapshot):
                assert ['this', 'will', 'fail'] == snapshot
            """
        ),
        "updated_3": (
            """
            def test_updated_3(snapshot):
                assert snapshot == ['this', 'will', 'be', 'too', 'much']
            """
        ),
    }
    return {**testcases, **updated_testcases}


def test_missing_snapshots(testdir, testcases):
    testdir.makepyfile(test_file=testcases["used"])
    result = testdir.runpytest("-v")
    assert "Snapshot does not exist" in clean_output(result.stdout.str())
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
    result_stdout = clean_output(result.stdout.str())
    assert "5 snapshots generated" in result_stdout
    assert "snapshots unused" not in result_stdout
    assert result.ret == 0


def test_failing_snapshots(stubs, testcases_updated):
    testdir = stubs[1]
    testdir.makepyfile(test_file="\n\n".join(testcases_updated.values()))
    result = testdir.runpytest("-v")
    result_stdout = clean_output(result.stdout.str())
    assert "2 snapshots passed" in result_stdout
    assert "3 snapshots failed" in result_stdout
    expected_strings = [
        # 1
        "- - be",
        "+ - not",
        "- - updated",
        "+ - match",
        # 2
        "- - be",
        "+ - fail",
        "- - updated",
        # 3
        "- - updated",
        "+ - too",
        "+ - much",
    ]
    for string in expected_strings:
        assert string in result_stdout
    assert result.ret == 1


def test_updated_snapshots(stubs, testcases_updated):
    testdir = stubs[1]
    testdir.makepyfile(test_file="\n\n".join(testcases_updated.values()))
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert "2 snapshots passed" in result_stdout
    assert "3 snapshots updated" in result_stdout
    assert result.ret == 0


def test_unused_snapshots(stubs):
    _, testdir, tests, _ = stubs
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v")
    result_stdout = clean_output(result.stdout.str())
    assert "snapshots generated" not in result_stdout
    assert "4 snapshots passed" in result_stdout
    assert "1 snapshot unused" in result_stdout
    assert result.ret == 0


def test_removed_snapshots(stubs):
    _, testdir, tests, filepath = stubs
    assert os.path.isfile(filepath)
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert "snapshot unused" not in result_stdout
    assert "1 snapshot deleted" in result_stdout
    assert result.ret == 0
    assert os.path.isfile(filepath)


def test_removed_snapshot_file(stubs):
    _, testdir, tests, filepath = stubs
    assert os.path.isfile(filepath)
    testdir.makepyfile(test_file=tests["inject"])
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert "snapshots unused" not in result_stdout
    assert "5 snapshots deleted" in result_stdout
    assert result.ret == 0
    assert not os.path.isfile(filepath)


def test_removed_empty_snapshot_file_only(stubs):
    _, testdir, _, filepath = stubs
    empty_filepath = os.path.join(os.path.dirname(filepath), "test_empty.yaml")
    with open(empty_filepath, "w") as empty_snapfile:
        empty_snapfile.write("")
    assert os.path.isfile(empty_filepath)
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert os.path.relpath(filepath) not in result_stdout
    assert "1 snapshot deleted" in result_stdout
    assert result.ret == 0
    assert os.path.isfile(filepath)
    assert not os.path.isfile(empty_filepath)
