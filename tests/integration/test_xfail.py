def test_no_failure_printed_if_all_failures_xfailed(testdir, plugin_args):
    testdir.makepyfile(
        test_file=(
            """
        import pytest

        @pytest.mark.xfail(reason="Failure expected.")
        def test_a(snapshot):
            assert snapshot == 'does-not-exist'
        """
        )
    )
    result = testdir.runpytest("-v", *plugin_args)
    result.stdout.no_re_match_line(r".*snapshot failed*")
    assert result.ret == 0


def test_failures_printed_if_only_some_failures_xfailed(
    testdir, plugin_args_fails_xdist
):
    testdir.makepyfile(
        test_file=(
            """
        import pytest

        @pytest.mark.xfail(reason="Failure expected.")
        def test_a(snapshot):
            assert snapshot == 'does-not-exist'

        def test_b(snapshot):
            assert snapshot == 'other'
        """
        )
    )
    result = testdir.runpytest("-v", *plugin_args_fails_xdist)
    result.stdout.re_match_lines((r".*1 snapshot failed*",))
    result.stdout.re_match_lines((r".*1 snapshot xfailed*",))
    assert result.ret == 1


def test_failure_printed_if_xfail_does_not_run(testdir, plugin_args_fails_xdist):
    testdir.makepyfile(
        test_file=(
            """
        import pytest

        @pytest.mark.xfail(False, reason="Failure expected.")
        def test_a(snapshot):
            assert snapshot == 'does-not-exist'
        """
        )
    )
    result = testdir.runpytest("-v", *plugin_args_fails_xdist)
    result.stdout.re_match_lines((r".*1 snapshot failed*",))
    result.stdout.no_re_match_line(r".*1 snapshot xfailed*")
    assert result.ret == 1
