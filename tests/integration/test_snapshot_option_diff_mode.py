import pytest


@pytest.fixture
def testfile(testdir) -> pytest.Testdir:
    testdir.makepyfile(
        test_file=(
            """
            def test_case(snapshot):
                assert snapshot == "some-value"
            """
        ),
    )
    return testdir


def test_diff_mode_disabled_does_not_print_diff(
    testfile,
):
    # Generate initial snapshot
    result = testfile.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"1 snapshot generated\.",))
    assert result.ret == 0

    # Modify snapshot to generate diff
    testfile.makepyfile(
        test_file=(
            """
            def test_case(snapshot):
                assert snapshot == "some-other-value"
            """
        ),
    )

    # With diff we expect to see "some-other-value"
    result = testfile.runpytest("-v", "--snapshot-diff-mode=detailed")
    result.stdout.re_match_lines(
        (
            r".*- 'some-value'",
            r".*\+ 'some-other-value'",
        )
    )
    assert result.ret == 1

    # Without diff we do not expect to see "some-other-value"
    result = testfile.runpytest("-v", "--snapshot-diff-mode=disabled")
    result.stdout.no_re_match_line(r".*- 'some-value'")
    result.stdout.no_re_match_line(r".*\+ 'some-other-value'")
    assert result.ret == 1
