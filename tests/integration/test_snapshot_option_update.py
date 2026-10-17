import sys
from pathlib import Path

import pytest


@pytest.fixture
def testcases_initial():
    return {
        "test_used": (
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, 2, 3])
            def test_used(snapshot, actual):
                assert snapshot == actual

            def test_used1(snapshot):
                assert snapshot == 'unused'
                assert 'unused' == snapshot
            """
        ),
        "test_updated_1": (
            """
            def test_updated_1(snapshot):
                assert snapshot == ['this', 'will', 'be', 'updated']
            """
        ),
        "test_updated_2": (
            """
            def test_updated_2(snapshot):
                assert ['this', 'will', 'be', 'updated'] == snapshot
            """
        ),
        "test_updated_3": (
            """
            def test_updated_3(snapshot):
                assert snapshot == ['this', 'will', 'be', 'updated']
            """
        ),
        "test_updated_4": (
            """
            def test_updated_4(snapshot):
                assert snapshot == "single line change"
            """
        ),
        "test_updated_5": (
            """
            def test_updated_5(snapshot):
                assert snapshot == '''
                multiple line changes
                with some lines staying the same
                intermittent changes that have to be ignore by the differ output
                because when there are a lot of changes you only want to see changes
                you do not want to see this line
                or this line
                this line should not show up because new lines are normalised\\r\\n
                \x1b[38;5;1mthis line should show up because it changes color\x1b[0m
                '''
            """
        ),
    }


@pytest.fixture
def testcases_updated(testcases_initial):
    updates = {
        "test_updated_1": (
            """
            def test_updated_1(snapshot):
                assert snapshot == ['this', 'will', 'not', 'match']
            """
        ),
        "test_updated_2": (
            """
            def test_updated_2(snapshot):
                assert ['this', 'will', 'fail'] == snapshot
            """
        ),
        "test_updated_3": (
            """
            def test_updated_3(snapshot):
                assert snapshot == ['this', 'will', 'be', 'too', 'much']
            """
        ),
        "test_updated_4": (
            """
            def test_updated_4(snapshot):
                assert snapshot == "sing line changeling"
            """
        ),
        "test_updated_5": (
            """
            def test_updated_5(snapshot):
                assert snapshot == '''
                multiple line changes
                with some lines not staying the same
                intermittent changes so unchanged lines have to be ignored by the differ
                cause when there are a lot of changes you only want to see what changed
                you do not want to see this line
                or this line
                this line should not show up because new lines are normalised\\n
                \x1b[38;5;3mthis line should show up because it changes color\x1b[0m
                and this line does not exist in the first one
                '''
            """
        ),
    }
    return {**testcases_initial, **updates}


@pytest.fixture
def run_testcases(testdir, testcases_initial):
    sys.path.append(str(testdir.tmpdir))
    testdir.makepyfile(**testcases_initial)
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"10 snapshots generated.",))
    assert "Can not relate snapshot name" not in result.stdout.str()

    return result, testdir, testcases_initial


def test_update_failure_shows_snapshot_diff(
    run_testcases, testcases_updated, plugin_args_fails_xdist
):
    testdir = run_testcases[1]
    testdir.makepyfile(**testcases_updated)
    result = testdir.runpytest("-vv", *plugin_args_fails_xdist)
    result.stdout.re_match_lines(
        (
            r".*assert snapshot == \['this', 'will', 'not', 'match'\]",
            r".*AssertionError: assert \[- snapshot\] == \[\+ received\]",
            r".*    list\(\[",
            r".*     ...",
            r".*      'will',",
            r".*  -   'be',",
            r".*  -   'updated',",
            r".*  \+   'not',",
            r".*  \+   'match',",
            r".*    \]",
            r".*assert \['this', 'will', 'fail'\] == snapshot",
            r".*AssertionError: assert \[\+ received\] == \[- snapshot\]",
            r".*    list\(\[",
            r".*     ...",
            r".*      'will',",
            r".*  -   'be',",
            r".*  \+   'fail',",
            r".*  -   'updated',",
            r".*    \]",
            r".*assert snapshot == \['this', 'will', 'be', 'too', 'much'\]",
            r".*AssertionError: assert \[- snapshot\] == \[\+ received\]",
            r".*    list\(\[",
            r".*     ...",
            r".*      'be',",
            r".*  -   'updated',",
            r".*  \+   'too',",
            r".*  \+   'much',",
            r".*    \]",
            r".*assert snapshot == \"sing line changeling\"",
            r".*AssertionError: assert \[- snapshot\] == \[\+ received\]",
            r".*  - 'single line change'",
            r".*  \+ 'sing line changeling'",
            r".*AssertionError: assert \[- snapshot\] == \[\+ received\]",
            r".*    '",
            r".*      ...",
            r".*        multiple line changes",
            r".*  -     with some lines staying the same",
            r".*  \+     with some lines not staying the same",
            r".*  -     intermittent changes that have to be ignore by the differ out",
            r".*  \+     intermittent changes so unchanged lines have to be ignored b",
            r".*  -     because when there are a lot of changes you only want to see ",
            r".*  \+     cause when there are a lot of changes you only want to see w",
            r".*        you do not want to see this line",
            r".*      ...",
            r".*    ",
            r".*  -     \[38;5;1mthis line should show up because it changes color",
            r".*  \+     \[38;5;3mthis line should show up because it changes color",
            r".*  \+     and this line does not exist in the first one",
            r".*        ",
            r".*    '",
        )
    )
    assert result.ret == 1


def test_update_success_shows_snapshot_report(
    run_testcases, testcases_updated, plugin_args
):
    testdir = run_testcases[1]
    testdir.makepyfile(**testcases_updated)
    result = testdir.runpytest("-v", "--snapshot-update", *plugin_args)
    result.stdout.re_match_lines((r"5 snapshots passed\. 5 snapshots updated\.",))
    assert result.ret == 0


def test_update_targets_only_selected_parametrized_tests_for_update_dash_m(
    run_testcases, plugin_args
):
    updated_tests = {
        "test_used": (
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, "2"])
            def test_used(snapshot, actual):
                assert snapshot == actual
            """
        ),
    }
    testdir = run_testcases[1]
    testdir.makepyfile(**updated_tests)
    result = testdir.runpytest(
        "-v", "--snapshot-update", *plugin_args, "-m", "parametrize"
    )
    result.stdout.re_match_lines(
        (
            r"1 snapshot passed\. 1 snapshot updated\. 1 unused snapshot deleted\.",
            r"Deleted test_used\[3\] \(__snapshots__[\\/]test_used.ambr\)",
        )
    )
    snapshot_path = [testdir.tmpdir, "__snapshots__"]
    assert Path(*snapshot_path, "test_used.ambr").exists()
    assert Path(*snapshot_path, "test_updated_1.ambr").exists()


def test_update_targets_only_selected_parametrized_tests_for_update_dash_k(
    run_testcases, plugin_args
):
    updated_tests = {
        "test_used": (
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, "2", 3])
            def test_used(snapshot, actual):
                assert snapshot == actual
            """
        ),
    }
    testdir = run_testcases[1]
    testdir.makepyfile(**updated_tests)
    result = testdir.runpytest(
        "-v", "--snapshot-update", *plugin_args, "-k", "test_used[2]"
    )
    result.stdout.re_match_lines((r"1 snapshot updated\.",))
    assert "Deleted" not in result.stdout.str()
    snapshot_path = [testdir.tmpdir, "__snapshots__"]
    assert Path(*snapshot_path, "test_used.ambr").exists()
    assert Path(*snapshot_path, "test_updated_1.ambr").exists()


def test_update_targets_only_selected_parametrized_tests_for_removal_dash_k(
    run_testcases, plugin_args
):
    updated_tests = {
        "test_used": (
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, 2])
            def test_used(snapshot, actual):
                assert snapshot == actual
            """
        ),
    }
    testdir = run_testcases[1]
    testdir.makepyfile(**updated_tests)
    result = testdir.runpytest(
        "-v", "--snapshot-update", *plugin_args, "-k", "test_used["
    )
    result.stdout.re_match_lines(
        (
            r"2 snapshots passed\. 1 unused snapshot deleted\.",
            r"Deleted test_used\[3\] \(__snapshots__[\\/]test_used\.ambr\)",
        )
    )
    snapshot_path = [testdir.tmpdir, "__snapshots__"]
    assert Path(*snapshot_path, "test_used.ambr").exists()
    assert Path(*snapshot_path, "test_updated_1.ambr").exists()


def test_update_no_cleanup_keeps_unused_snapshots(run_testcases, plugin_args):
    updated_tests = {
        "test_used": (
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, 2])
            def test_used(snapshot, actual):
                assert snapshot == actual
            """
        ),
    }
    testdir = run_testcases[1]
    testdir.makepyfile(**updated_tests)
    result = testdir.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-no-cleanup",
        *plugin_args,
        "-k",
        "test_used[",
    )
    result.stdout.re_match_lines((r"2 snapshots passed\. 1 snapshot unused\.",))
    assert "deleted" not in result.stdout.str().lower()

    # The unused snapshot is reported but kept on disk.
    snapshot_file = Path(testdir.tmpdir, "__snapshots__", "test_used.ambr")
    assert snapshot_file.exists()
    assert "test_used[3]" in snapshot_file.read_text()


def test_update_targets_only_selected_class_tests_dash_k(testdir, plugin_args):
    test_content = """
        import pytest

        class TestClass:
            def test_case_1(self, snapshot):
                assert snapshot == 1

            def test_case_2(self, snapshot):
                assert snapshot == 2
        """

    testdir.makepyfile(test_content=test_content)
    testdir.runpytest("-v", "--snapshot-update")
    assert Path(testdir.tmpdir, "__snapshots__", "test_content.ambr").exists()

    result = testdir.runpytest(
        "test_content.py", "-v", *plugin_args, "-k", "test_case_2"
    )
    result.stdout.re_match_lines((r"1 snapshot passed\.",))
    assert "snapshot unused" not in result.stdout.str()


def test_update_targets_only_selected_module_tests_dash_k(testdir, plugin_args):
    test_content = """
        import pytest

        def test_case_1(snapshot):
            assert snapshot == 1

        def test_case_2(snapshot):
            assert snapshot == 2
        """

    testdir.makepyfile(test_content=test_content)
    testdir.runpytest("-v", "--snapshot-update")
    assert Path(testdir.tmpdir, "__snapshots__", "test_content.ambr").exists()

    result = testdir.runpytest(
        "test_content.py", "-v", *plugin_args, "-k", "test_case_2"
    )
    result.stdout.re_match_lines((r"1 snapshot passed\.",))
    assert "snapshot unused" not in result.stdout.str()


def test_update_targets_only_selected_module_tests_nodes(run_testcases, plugin_args):
    testdir = run_testcases[1]
    snapfile_empty = Path("__snapshots__", "empty_snapfile.ambr")
    testdir.makefile(".ambr", **{str(snapfile_empty): ""})
    testfile = Path(testdir.tmpdir, "test_used.py")
    result = testdir.runpytest(
        "-v", f"{testfile}::test_used", "--snapshot-update", *plugin_args
    )
    result.stdout.re_match_lines((r"3 snapshots passed\.",))
    assert "unused" not in result.stdout.str()
    assert "updated" not in result.stdout.str()
    assert "deleted" not in result.stdout.str()
    assert result.ret == 0
    assert snapfile_empty.exists()


def test_update_targets_only_selected_module_tests_nodes_pyargs(
    run_testcases, plugin_args_fails_xdist
):
    testdir = run_testcases[1]
    snapfile_empty = Path("__snapshots__", "empty_snapfile.ambr")
    testdir.makefile(".ambr", **{str(snapfile_empty): ""})
    result = testdir.runpytest(
        "-v",
        "--snapshot-update",
        *plugin_args_fails_xdist,
        "--pyargs",
        "test_used::test_used",
    )
    result.stdout.re_match_lines((r"3 snapshots passed\.",))
    assert "unused" not in result.stdout.str()
    assert "updated" not in result.stdout.str()
    assert "deleted" not in result.stdout.str()
    assert result.ret == 0
    assert snapfile_empty.exists()


def test_update_targets_only_selected_module_tests_file_for_update(
    run_testcases, plugin_args
):
    testdir = run_testcases[1]
    snapfile_empty = Path("__snapshots__", "empty_snapfile.ambr")
    testdir.makefile(".ambr", **{str(snapfile_empty): ""})
    testdir.makepyfile(
        test_used=(
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, 2, 3])
            def test_used(snapshot, actual):
                assert snapshot == actual
            """
        )
    )
    result = testdir.runpytest("-v", "test_used.py", "--snapshot-update", *plugin_args)
    result.stdout.re_match_lines(
        (
            r"3 snapshots passed\. 2 unused snapshots deleted\.",
            r"Deleted test_used1, test_used1\.1 \(__snapshots__[\\/]test_used\.ambr\)",
        )
    )
    assert result.ret == 0
    assert snapfile_empty.exists()
    assert Path("__snapshots__", "test_used.ambr").exists()


def test_update_targets_only_selected_module_tests_file_for_removal(
    run_testcases, plugin_args
):
    testdir = run_testcases[1]
    testdir.makepyfile(
        test_used=(
            """
            def test_used(snapshot):
                assert True
            """
        ),
    )
    snapfile_empty = Path("__snapshots__", "empty_snapfile.ambr")
    testdir.makefile(".ambr", **{str(snapfile_empty): ""})
    result = testdir.runpytest("-v", "test_used.py", "--snapshot-update", *plugin_args)
    result.stdout.re_match_lines(
        (
            r"5 unused snapshots deleted\.",
            (
                r"Deleted test_used1, test_used1\.1, test_used\[1\], test_used\[2\]"
                r", test_used\[3\] \(__snapshots__[\\/]test_used\.ambr\)"
            ),
        )
    )
    assert result.ret == 0
    assert snapfile_empty.exists()
    assert not Path("__snapshots__", "test_used.ambr").exists()


def test_update_removes_empty_snapshot_collection_only(run_testcases, plugin_args):
    testdir = run_testcases[1]
    snapfile_empty = Path("__snapshots__", "empty_snapfile.ambr")
    testdir.makefile(".ambr", **{str(snapfile_empty): ""})
    assert snapfile_empty.exists()
    result = testdir.runpytest("-v", "--snapshot-update", *plugin_args)
    result.stdout.re_match_lines(
        (
            r"10 snapshots passed\. 1 unused snapshot deleted\.",
            (
                r"Deleted empty snapshot collection "
                r"\(__snapshots__[\\/]empty_snapfile\.ambr\)"
            ),
        )
    )
    assert result.ret == 0
    assert not snapfile_empty.exists()
    assert Path("__snapshots__", "test_used.ambr").exists()


def test_update_removes_hanging_snapshot_collection_file(run_testcases, plugin_args):
    testdir = run_testcases[1]
    snapfile_used = Path("__snapshots__", "test_used.ambr")
    snapfile_hanging = Path("__snapshots__", "hanging_snapfile.abc")
    testdir.makefile(".abc", **{str(snapfile_hanging): ""})
    assert snapfile_hanging.exists()
    result = testdir.runpytest("-v", "--snapshot-update", *plugin_args)
    result.stdout.re_match_lines(
        (
            r"10 snapshots passed\. 1 unused snapshot deleted\.",
            (
                r"Deleted unknown snapshot collection "
                r"\(__snapshots__[\\/]hanging_snapfile\.abc\)"
            ),
        )
    )
    assert f"{snapfile_used}" not in result.stdout.str()
    assert result.ret == 0
    assert snapfile_used.exists()
    assert not snapfile_hanging.exists()


@pytest.mark.parametrize(
    "selection",
    [
        "full",
        "partial",
        "no_snapshots",
        "unknown_extension",
        "mixed_amber",
        "directory",
    ],
)
def test_update_removes_single_file_collection_of_deleted_test_file(
    testdir, plugin_args, selection
):
    extension = (
        "syrupy.extensions.single_file.SingleFileAmberSnapshotExtension"
        if selection == "mixed_amber"
        else "syrupy.extensions.json.JSONSnapshotExtension"
    )
    suffix = "ambr" if selection == "mixed_amber" else "json"
    testdir.makepyfile(
        test_foo=(
            """
            def test_foo(snapshot):
                assert snapshot == "foo"
            """
        ),
        test_bar=(
            """
            def test_bar(snapshot):
                assert snapshot == "bar"
            """
        ),
    )
    testdir.runpytest(
        "-v",
        "--snapshot-update",
        f"--snapshot-default-extension={extension}",
    )
    snapshot_dir = Path(testdir.tmpdir, "__snapshots__", "test_bar")
    snapshot_file = Path(snapshot_dir, f"test_bar.{suffix}")
    assert snapshot_file.exists()

    # Deleting the test file leaves no assertion to reveal the snapshot site;
    # the orphaned collection is still found through the remaining test file.
    Path(testdir.tmpdir, "test_bar.py").unlink()
    if selection in {"no_snapshots", "unknown_extension"}:
        testdir.makepyfile(test_foo="def test_foo():\n    assert True")
    elif selection == "mixed_amber":
        testdir.makepyfile(
            test_foo=(
                "from syrupy.extensions.amber import AmberSnapshotExtension\n"
                "def test_foo(snapshot):\n"
                '    assert snapshot.use_extension(AmberSnapshotExtension) == "foo"'
            )
        )
    result = testdir.runpytest(
        "-v",
        *({"partial": ["test_foo.py"], "directory": ["."]}.get(selection, [])),
        "--snapshot-update",
        *(
            [f"--snapshot-default-extension={extension}"]
            if selection != "unknown_extension"
            else []
        ),
        *plugin_args,
    )
    assert result.ret == 0
    if selection == "partial":
        assert snapshot_dir.exists()
        assert "unused" not in result.stdout.str()
    else:
        assert not snapshot_dir.exists(), (
            "orphaned single-file collection directory remains"
        )
    assert Path(
        testdir.tmpdir, "__snapshots__", "test_foo", f"test_foo.{suffix}"
    ).exists() == (selection in {"full", "partial", "directory"})
    if selection == "mixed_amber":
        assert Path(testdir.tmpdir, "__snapshots__", "test_foo.ambr").exists()


def test_update_removes_collection_dir_without_snapshot_tests(testdir, plugin_args):
    testdir.makepyfile(
        **{
            "foo/test_foo": (
                """
                def test_foo(snapshot):
                    assert snapshot == "foo"
                """
            ),
            "bar/test_bar": (
                """
                def test_bar(snapshot):
                    assert snapshot == "bar"
                """
            ),
        }
    )
    testdir.runpytest("-v", "--snapshot-update")
    snapshot_file = Path(testdir.tmpdir, "bar", "__snapshots__", "test_bar.ambr")
    assert snapshot_file.exists()

    # The test file survives but no longer uses the fixture; its collection
    # is still found through the other tests collected in its directory.
    testdir.makepyfile(
        **{
            "bar/test_bar": (
                """
                def test_bar():
                    assert True
                """
            ),
        }
    )
    result = testdir.runpytest("-v", "--snapshot-update", *plugin_args)
    result.stdout.re_match_lines(
        (
            r"1 snapshot passed\. 1 unused snapshot deleted\.",
            r"Deleted test_bar \(bar[\\/]__snapshots__[\\/]test_bar\.ambr\)",
        )
    )
    assert result.ret == 0
    assert not snapshot_file.exists()
    assert Path(testdir.tmpdir, "foo", "__snapshots__", "test_foo.ambr").exists()


def test_update_preserves_deselected_snapshots_in_discovered_collection(
    testdir, plugin_args
):
    testdir.makepyfile(
        **{
            "foo/test_foo": 'def test_foo(snapshot):\n    assert snapshot == "foo"',
            "bar/test_bar": (
                'def test_removed(snapshot):\n    assert snapshot == "bar"\n'
                'def test_valid(snapshot):\n    assert snapshot == "valid"'
            ),
        }
    )
    assert testdir.runpytest("--snapshot-update").ret == 0
    testdir.makepyfile(
        **{
            "bar/test_bar": (
                "def test_removed():\n    assert True\n"
                'def test_valid(snapshot):\n    assert snapshot == "valid"'
            ),
        }
    )
    result = testdir.runpytest(
        "--snapshot-update", "-k", "test_foo or test_removed", *plugin_args
    )
    assert result.ret == 0
    collection = Path(testdir.tmpdir, "bar", "__snapshots__", "test_bar.ambr")
    assert collection.exists(), "deselected snapshot collection was deleted"
    assert "# name: test_valid" in collection.read_text()
    assert "# name: test_removed" not in collection.read_text()
