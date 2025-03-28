import pytest


@pytest.fixture
def testcases():
    return {
        "a": (
            """
            def test_a(snapshot):
                assert snapshot == b"a"
            """
        ),
        "b": (
            """
            def test_b(snapshot):
                assert snapshot == b"b"
            """
        ),
        "a_suffix": (
            """
            def test_a_suffix(snapshot):
                assert snapshot == b"a_suffix"
            """
        ),
    }


@pytest.fixture
def run_testcases(testdir, testcases):
    pyfile_content = "\n\n".join(testcases.values())
    testdir.makepyfile(
        test_1=pyfile_content, test_2=pyfile_content, test_1_suffix=pyfile_content
    )
    result = testdir.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-default-extension",
        "syrupy.extensions.single_file.SingleFileSnapshotExtension",
    )
    result.stdout.re_match_lines((r"9 snapshots generated\.",))
    return testdir, testcases


def test_run_all(run_testcases, plugin_args_fails_xdist):
    testdir, testcases = run_testcases
    result = testdir.runpytest(
        "-v",
        "--snapshot-default-extension",
        "syrupy.extensions.single_file.SingleFileSnapshotExtension",
        *plugin_args_fails_xdist,
    )
    result.stdout.re_match_lines(("9 snapshots passed",))
    assert result.ret == 0


def test_run_single_file(run_testcases, plugin_args_fails_xdist):
    testdir, testcases = run_testcases
    result = testdir.runpytest(
        "-v",
        "--snapshot-default-extension",
        "syrupy.extensions.single_file.SingleFileSnapshotExtension",
        "test_1.py",
        *plugin_args_fails_xdist,
    )
    result.stdout.re_match_lines(("3 snapshots passed",))
    assert result.ret == 0


def test_run_single_test_case_in_file(run_testcases, plugin_args_fails_xdist):
    testdir, testcases = run_testcases
    result = testdir.runpytest(
        "-v",
        "--snapshot-default-extension",
        "syrupy.extensions.single_file.SingleFileSnapshotExtension",
        "test_2.py::test_a",
        *plugin_args_fails_xdist,
    )
    result.stdout.re_match_lines(("1 snapshot passed",))
    assert result.ret == 0


def test_run_all_but_one(run_testcases, plugin_args_fails_xdist):
    testdir, testcases = run_testcases
    result = testdir.runpytest(
        "-v",
        "--snapshot-details",
        "--snapshot-default-extension",
        "syrupy.extensions.single_file.SingleFileSnapshotExtension",
        "test_1.py",
        "test_2.py::test_a",
        *plugin_args_fails_xdist,
    )
    result.stdout.re_match_lines(("4 snapshots passed",))
    assert result.ret == 0


def test_run_both_files_by_node(run_testcases, plugin_args_fails_xdist):
    testdir, testcases = run_testcases
    result = testdir.runpytest(
        "-v",
        "--snapshot-details",
        "--snapshot-default-extension",
        "syrupy.extensions.single_file.SingleFileSnapshotExtension",
        "test_1.py::test_a",
        "test_2.py::test_a",
        *plugin_args_fails_xdist,
    )
    result.stdout.re_match_lines(("2 snapshots passed",))
    assert result.ret == 0


def test_run_both_files_by_node_2(run_testcases, plugin_args_fails_xdist):
    testdir, testcases = run_testcases
    result = testdir.runpytest(
        "-v",
        "--snapshot-details",
        "--snapshot-default-extension",
        "syrupy.extensions.single_file.SingleFileSnapshotExtension",
        "test_1.py::test_b",
        "test_2.py::test_a",
        *plugin_args_fails_xdist,
    )
    result.stdout.re_match_lines(("2 snapshots passed",))
    assert result.ret == 0
