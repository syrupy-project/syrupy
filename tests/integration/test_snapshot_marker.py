from pathlib import Path


def assert_marker_outcomes(result, plugin_args, *, passed, deselected):
    if plugin_args == ["--numprocesses", "2"]:
        result.assert_outcomes(passed=passed)
    else:
        result.assert_outcomes(passed=passed, deselected=deselected)


def test_marker_selects_direct_and_indirect_snapshot_tests(testdir, plugin_args):
    testdir.makepyfile(
        test_selection="""
            import pytest

            @pytest.fixture
            def snapshot_wrapper(snapshot):
                return snapshot

            def test_direct(snapshot):
                assert snapshot == "direct"

            def test_indirect(snapshot_wrapper):
                assert snapshot_wrapper == "indirect"

            def test_without_snapshot():
                raise AssertionError("ordinary test should be deselected")
        """
    )
    initial = testdir.runpytest(
        "-v",
        "--snapshot-update",
        "test_selection.py::test_direct",
        "test_selection.py::test_indirect",
    )
    initial.assert_outcomes(passed=2)

    result = testdir.runpytest(
        "-v",
        "--strict-markers",
        "--snapshot-update",
        "-m",
        "syrupy_snapshot",
        *plugin_args,
    )

    assert_marker_outcomes(result, plugin_args, passed=2, deselected=1)
    result.stdout.re_match_lines((r"2 snapshots passed\.",))
    snapshot_file = Path(testdir.tmpdir, "__snapshots__", "test_selection.ambr")
    assert snapshot_file.exists()
    assert "direct" in snapshot_file.read_text()
    assert "indirect" in snapshot_file.read_text()


def test_marker_combines_with_existing_mark_and_keyword_filters(testdir, plugin_args):
    testdir.makeini(
        """
        [pytest]
        markers = selected: tests selected for this regression
        """
    )
    testdir.makepyfile(
        test_selection="""
            import pytest

            @pytest.mark.selected
            def test_snapshot_selected(snapshot):
                assert snapshot == "selected"

            @pytest.mark.selected
            def test_snapshot_other(snapshot):
                raise AssertionError("filtered by -k")

            @pytest.mark.selected
            def test_ordinary_selected():
                raise AssertionError("filtered by the Syrupy marker")
        """
    )

    result = testdir.runpytest(
        "-v",
        "--snapshot-update",
        "-m",
        "syrupy_snapshot and selected",
        "-k",
        "snapshot_selected",
        *plugin_args,
    )

    assert_marker_outcomes(result, plugin_args, passed=1, deselected=2)
    result.stdout.re_match_lines((r"1 snapshot generated\.",))


def test_marker_filter_does_not_delete_snapshot_for_keyword_deselected_test(
    testdir, plugin_args
):
    testdir.makepyfile(
        test_selection="""
            def test_one(snapshot):
                assert snapshot == "one"

            def test_two(snapshot):
                assert snapshot == "two"
        """
    )
    initial = testdir.runpytest("-v", "--snapshot-update")
    initial.assert_outcomes(passed=2)

    result = testdir.runpytest(
        "-v",
        "--snapshot-update",
        "-m",
        "syrupy_snapshot",
        "-k",
        "test_one",
        *plugin_args,
    )

    assert_marker_outcomes(result, plugin_args, passed=1, deselected=1)
    output = result.stdout.str().lower()
    assert "unused" not in output
    assert "deleted" not in output
    snapshot_file = Path(testdir.tmpdir, "__snapshots__", "test_selection.ambr")
    assert "test_two" in snapshot_file.read_text()


def test_snapshot_update_without_marker_filter_runs_ordinary_tests(
    testdir, plugin_args
):
    testdir.makepyfile(
        test_selection="""
            def test_with_snapshot(snapshot):
                assert snapshot == "snapshot"

            def test_without_snapshot():
                assert True
        """
    )

    result = testdir.runpytest("-v", "--snapshot-update", *plugin_args)

    result.assert_outcomes(passed=2)
    assert "deselected" not in result.stdout.str()
