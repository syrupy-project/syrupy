from pathlib import Path

import pytest


# EqualsAssertionError comes from:
# https://github.com/JetBrains/intellij-community/blob/cd9bfbd98a7dca730fbc469156ce1ed30364afba/python/helpers/pycharm/teamcity/diff_tools.py#L53
@pytest.fixture
def mock_teamcity_diff_tools(testdir: "pytest.Testdir"):
    teamcity_pkg = testdir.mkpydir("teamcity")
    diff_tools_file = teamcity_pkg / Path("diff_tools.py")
    diff_tools_file.write_text(
        """
class EqualsAssertionError:
    def __init__(self, expected, actual, msg=None, preformated=False, real_exception=None): # noqa: E501
        self.real_exception = real_exception
        self.expected = expected
        self.actual = actual
        self.msg = str(msg)
    """,
        "utf-8",
    )


@pytest.mark.filterwarnings("default")
def test_logs_a_warning_if_unable_to_apply_patch(testdir, plugin_args):
    testdir.makepyfile(
        test_file="""
    def test_case(snapshot):
        assert snapshot == [1, 2]
    """
    )
    testdir.runpytest("-v", "--snapshot-update", *plugin_args)
    testdir.makepyfile(
        test_file="""
    def test_case(snapshot):
        assert snapshot == [1, 2, 3]
    """
    )

    result = testdir.runpytest("-v", "--snapshot-patch-pycharm-diff", *plugin_args)
    result.assert_outcomes(failed=1, passed=0, warnings=1)


@pytest.mark.filterwarnings("default")
def test_patches_pycharm_diff_tools_when_flag_set(
    testdir, mock_teamcity_diff_tools, plugin_args
):
    # Generate initial snapshot
    testdir.makepyfile(
        test_file="""
    def test_case(snapshot):
        assert snapshot == [1, 2]
    """
    )
    testdir.runpytest("-v", "--snapshot-update", *plugin_args)

    # Generate diff and mimic EqualsAssertionError being thrown
    testdir.makepyfile(
        test_file="""

    def test_case(snapshot):
        try:
            assert snapshot == [1, 2, 3]
        except:
            from teamcity.diff_tools import EqualsAssertionError

            err = EqualsAssertionError(expected=snapshot, actual=[1,2,3])
            print("Expected:", repr(err.expected))
            print("Actual:", repr(err.actual))
            raise
    """
    )

    result = testdir.runpytest("-v", "--snapshot-patch-pycharm-diff", *plugin_args)
    # No warnings because patch should have been successful
    result.assert_outcomes(failed=1, passed=0, warnings=0)

    result.stdout.re_match_lines(
        [
            r"Expected: 'list([\n  1,\n  2,\n])'",
            # Actual is the amber-style list representation
            r"Actual: 'list([\n  1,\n  2,\n  3,\n])'",
        ]
    )


@pytest.mark.filterwarnings("default")
def test_patches_pycharm_diff_tools_when_flag_set_and_snapshot_on_right(
    testdir, mock_teamcity_diff_tools, plugin_args
):
    # Generate initial snapshot
    testdir.makepyfile(
        test_file="""
    def test_case(snapshot):
        assert [1, 2] == snapshot
    """
    )
    testdir.runpytest("-v", "--snapshot-update", *plugin_args)

    # Generate diff and mimic EqualsAssertionError being thrown
    testdir.makepyfile(
        test_file="""

    def test_case(snapshot):
        try:
            assert [1, 2, 3] == snapshot
        except:
            from teamcity.diff_tools import EqualsAssertionError

            err = EqualsAssertionError(expected=[1,2,3], actual=snapshot)
            print("Expected:", repr(err.expected))
            print("Actual:", repr(err.actual))
            raise
    """
    )

    result = testdir.runpytest("-v", "--snapshot-patch-pycharm-diff", *plugin_args)
    # No warnings because patch should have been successful
    result.assert_outcomes(failed=1, passed=0, warnings=0)

    result.stdout.re_match_lines(
        [
            r"Expected: 'list([\n  1,\n  2,\n])'",
            # Actual is the amber-style list representation
            r"Actual: 'list([\n  1,\n  2,\n  3,\n])'",
        ]
    )


@pytest.mark.filterwarnings("default")
def test_it_does_not_patch_pycharm_diff_tools_by_default(
    testdir, mock_teamcity_diff_tools, plugin_args
):
    # Generate initial snapshot
    testdir.makepyfile(
        test_file="""
    def test_case(snapshot):
        assert snapshot == [1, 2]
    """
    )
    testdir.runpytest("-v", "--snapshot-update", *plugin_args)

    # Generate diff and mimic EqualsAssertionError being thrown
    testdir.makepyfile(
        test_file="""

    def test_case(snapshot):
        try:
            assert snapshot == [1, 2, 3]
        except:
            from teamcity.diff_tools import EqualsAssertionError

            err = EqualsAssertionError(expected=snapshot, actual=[1,2,3])
            print("Expected:", repr(str(err.expected)))
            print("Actual:", repr(str(err.actual)))
            raise
    """
    )

    result = testdir.runpytest("-v", *plugin_args)
    # No warnings because patch should have been successful
    result.assert_outcomes(failed=1, passed=0, warnings=0)

    result.stdout.re_match_lines(
        [
            r"Expected: 'list([\n  1,\n  2,\n])'",
            # Actual is the original list's repr. No newlines or amber-style list prefix
            r"Actual: '[1, 2, 3]'",
        ]
    )


@pytest.mark.filterwarnings("default")
def test_it_has_no_impact_on_non_syrupy_assertions(
    testdir, mock_teamcity_diff_tools, plugin_args
):
    # Generate diff and mimic EqualsAssertionError being thrown
    testdir.makepyfile(
        test_file="""

    def test_case():
        try:
            assert [1, 3] == [1, 2, 3]
        except:
            from teamcity.diff_tools import EqualsAssertionError

            err = EqualsAssertionError(expected=[1,3], actual=[1,2,3])
            print("Expected:", repr(str(err.expected)))
            print("Actual:", repr(str(err.actual)))
            raise
    """
    )

    result = testdir.runpytest("-v", *plugin_args)
    # No warnings because patch should have been successful
    result.assert_outcomes(failed=1, passed=0, warnings=0)

    result.stdout.re_match_lines(
        [
            r"Expected: '[1, 3]'",
            r"Actual: '[1, 2, 3]'",
        ]
    )


@pytest.mark.filterwarnings("default")
def test_has_no_impact_on_real_exceptions_that_are_not_assertion_errors(
    testdir, mock_teamcity_diff_tools, plugin_args
):
    # Generate diff and mimic EqualsAssertionError being thrown
    testdir.makepyfile(
        test_file="""

    def test_case():
        try:
            assert [1, 3] == (1/0)
        except Exception as err:
            from teamcity.diff_tools import EqualsAssertionError

            err = EqualsAssertionError(
                expected=[1,3],
                actual=[1,2,3],
                real_exception=err
            )
            print("Expected:", repr(str(err.expected)))
            print("Actual:", repr(str(err.actual)))
            raise
    """
    )

    result = testdir.runpytest("-v", *plugin_args)
    # No warnings because patch should have been successful
    result.assert_outcomes(failed=1, passed=0, warnings=0)

    result.stdout.re_match_lines(
        [
            r"Expected: '[1, 3]'",
            r"Actual: '[1, 2, 3]'",
        ]
    )
