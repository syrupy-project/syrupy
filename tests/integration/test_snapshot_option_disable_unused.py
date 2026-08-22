import pytest


@pytest.fixture
def testcases():
    return {
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


@pytest.fixture
def run_testcases(testdir, testcases):
    pyfile_content = "\n\n".join(testcases.values())
    testdir.makepyfile(test_file=pyfile_content)
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    return testdir, testcases


def test_disable_unused_skips_failure(run_testcases, plugin_args):
    testdir, testcases = run_testcases
    testdir.makepyfile(test_file=testcases["used"])

    result = testdir.runpytest("-v", "--snapshot-disable-unused", *plugin_args)
    result.stdout.re_match_lines(
        (
            (
                r".*Unused snapshot detection is disabled "
                r"\(--snapshot-disable-unused\)\. This is not recommended\."
            ),
        )
    )
    result.stdout.no_fnmatch_line("*snapshot unused*")
    result.stdout.no_fnmatch_line("*snapshots unused*")
    assert result.ret == 0


def test_disable_unused_does_not_delete_on_update(run_testcases, plugin_args):
    testdir, testcases = run_testcases
    testdir.makepyfile(test_file=testcases["used"])

    result = testdir.runpytest(
        "-v", "--snapshot-update", "--snapshot-disable-unused", *plugin_args
    )
    result.stdout.re_match_lines(
        (
            (
                r".*Unused snapshot detection is disabled "
                r"\(--snapshot-disable-unused\)\. This is not recommended\."
            ),
        )
    )
    result.stdout.no_fnmatch_line("*unused snapshot deleted*")
    assert result.ret == 0

    snapshot_file = testdir.tmpdir.join("__snapshots__", "test_file.ambr")
    content = snapshot_file.read()
    assert "test_unused" in content
    assert "test_used" in content
