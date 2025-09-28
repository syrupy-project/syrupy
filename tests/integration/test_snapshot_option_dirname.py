from pathlib import Path

import pytest


@pytest.fixture
def testcases():
    return {
        "base": (
            """
            def test_a(snapshot):
                assert snapshot(name="xyz") == "case 1"
                assert snapshot(name="zyx") == "case 2"
            """
        ),
        "modified": (
            """
            def test_a(snapshot):
                assert snapshot(name="xyz") == "case 1"
                assert snapshot(name="zyx") == "case ??"
            """
        ),
    }


@pytest.fixture
def run_testcases(pytester, testcases) -> tuple[pytest.Pytester, dict[str, str]]:
    pytester.makepyfile(test_1=testcases["base"])
    result = pytester.runpytest(
        "-v",
        "--snapshot-dirname=snaps",
        "--snapshot-update",
    )
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    return pytester, testcases


def test_run_all(run_testcases, plugin_args_fails_xdist):
    pytester, _ = run_testcases
    result = pytester.runpytest(
        "-v", "--snapshot-dirname=snaps", *plugin_args_fails_xdist
    )
    result.stdout.re_match_lines(("2 snapshots passed",))
    assert result.ret == 0

    # Assert there's a snaps folder but no __snapshots__ folder
    expected_dir = pytester.path / Path("snaps")
    unexpected_dir = pytester.path / Path("__snapshots__")

    assert expected_dir.exists()
    assert not unexpected_dir.exists()


def test_failure(run_testcases, plugin_args_fails_xdist):
    pytester, testcases = run_testcases
    pytester.makepyfile(test_1=testcases["modified"])
    result = pytester.runpytest(
        "-vv", "--snapshot-dirname=snaps", *plugin_args_fails_xdist
    )
    result.stdout.re_match_lines(("1 snapshot failed. 1 snapshot passed.",))
    assert result.ret == 1

    # Assert there's a snaps folder but no __snapshots__ folder
    expected_dir = pytester.path / Path("snaps")
    unexpected_dir = pytester.path / Path("__snapshots__")

    assert expected_dir.exists()
    assert not unexpected_dir.exists()


def test_update(run_testcases, plugin_args_fails_xdist):
    pytester, testcases = run_testcases
    pytester.makepyfile(test_1=testcases["modified"])
    result = pytester.runpytest(
        "-v", "--snapshot-dirname=snaps", "--snapshot-update", *plugin_args_fails_xdist
    )
    assert "Can not relate snapshot name" not in str(result.stdout)
    result.stdout.re_match_lines(("1 snapshot passed. 1 snapshot updated.",))
    assert result.ret == 0

    # Assert there's a snaps folder but no __snapshots__ folder
    expected_dir = pytester.path / Path("snaps")
    unexpected_dir = pytester.path / Path("__snapshots__")

    assert expected_dir.exists()
    assert not unexpected_dir.exists()
