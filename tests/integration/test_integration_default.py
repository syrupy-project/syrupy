from pathlib import Path

import pytest


@pytest.fixture
def collection(testdir):
    tests = {
        "test_collected": (
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, 2, 3])
            def test_collected(snapshot, actual):
                assert snapshot == actual
            """
        ),
        "test_not_collected": (
            """
            def test_collected1(snapshot):
                assert snapshot == "hello"
            """
        ),
    }
    testdir.makepyfile(**tests)
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"4 snapshots generated."))
    testdir.makefile(".ambr", **{str(Path("__snapshots__", "other_snapfile")): ""})
    return testdir


def test_unused_snapshots_ignored_if_not_targeted_using_dash_m(collection):
    updated_tests = {
        "test_collected": (
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, "2"])
            def test_collected(snapshot, actual):
                assert snapshot == actual
            """
        ),
    }
    collection.makepyfile(**updated_tests)
    result = collection.runpytest("-v", "--snapshot-update", "-m", "parametrize")
    result.stdout.re_match_lines(
        (
            r"1 snapshot passed\. 1 snapshot updated\. 1 unused snapshot deleted\.",
            r"Deleted test_collected\[3\] \(__snapshots__[\\/]test_collected.ambr\)",
        )
    )
    snapshot_path = [collection.tmpdir, "__snapshots__"]
    assert Path(*snapshot_path, "test_not_collected.ambr").exists()
    assert Path(*snapshot_path, "other_snapfile.ambr").exists()


def test_unused_snapshots_ignored_if_not_targeted_using_dash_k(collection):
    updated_tests = {
        "test_collected": (
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, "2"])
            def test_collected(snapshot, actual):
                assert snapshot == actual
            """
        ),
    }
    collection.makepyfile(**updated_tests)
    result = collection.runpytest("-v", "--snapshot-update", "-k", "test_collected[")
    result.stdout.re_match_lines(
        (
            r"1 snapshot passed\. 1 snapshot updated\. 1 unused snapshot deleted\.",
            r"Deleted test_collected\[3\] \(__snapshots__[\\/]test_collected.ambr\)",
        )
    )
    snapshot_path = [collection.tmpdir, "__snapshots__"]
    assert Path(*snapshot_path, "test_not_collected.ambr").exists()
    assert Path(*snapshot_path, "other_snapfile.ambr").exists()


def test_unused_parameterized_ignored_if_not_targeted_using_dash_k(collection):
    updated_tests = {
        "test_collected": (
            """
            import pytest

            @pytest.mark.parametrize("actual", [1, 2])
            def test_collected(snapshot, actual):
                assert snapshot == actual
            """
        ),
    }
    collection.makepyfile(**updated_tests)
    result = collection.runpytest("-v", "--snapshot-update", "-k", "test_collected[")
    result.stdout.re_match_lines(
        (
            r"2 snapshots passed\. 1 unused snapshot deleted\.",
            r"Deleted test_collected\[3\] \(__snapshots__[\\/]test_collected\.ambr\)",
        )
    )
    snapshot_path = [collection.tmpdir, "__snapshots__"]
    assert Path(*snapshot_path, "test_not_collected.ambr").exists()
    assert Path(*snapshot_path, "other_snapfile.ambr").exists()


def test_only_updates_targeted_snapshot_in_class_for_single_file(testdir):
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

    snapshot_path = Path(testdir.tmpdir, "__snapshots__")
    assert snapshot_path.joinpath("test_content.ambr").exists()

    test_filepath = Path(testdir.tmpdir, "test_content.py")
    result = testdir.runpytest(str(test_filepath), "-v", "-k test_case_2")
    result_stdout = result.stdout.str()
    assert "1 snapshot passed" in result_stdout
    assert "snapshot unused" not in result_stdout


def test_only_updates_targeted_snapshot_for_single_file(testdir):
    test_content = """
        import pytest

        def test_case_1(snapshot):
            assert snapshot == 1

        def test_case_2(snapshot):
            assert snapshot == 2
        """

    testdir.makepyfile(test_content=test_content)
    testdir.runpytest("-v", "--snapshot-update")

    snapshot_path = Path(testdir.tmpdir, "__snapshots__")
    assert snapshot_path.joinpath("test_content.ambr").exists()

    test_filepath = Path(testdir.tmpdir, "test_content.py")
    result = testdir.runpytest(str(test_filepath), "-v", "-k test_case_2")
    result_stdout = result.stdout.str()
    assert "1 snapshot passed" in result_stdout
    assert "snapshot unused" not in result_stdout


def test_multiple_snapshots(testdir):
    test_content = """
        import pytest

        def test_case_1(snapshot):
            assert snapshot == 1
            assert snapshot == 2
        """

    testdir.makepyfile(test_content=test_content)
    result = testdir.runpytest("-v", "--snapshot-update")

    result_stdout = result.stdout.str()
    assert "Can not relate snapshot name" not in result_stdout


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
        "updated_4": (
            """
            def test_updated_4(snapshot):
                assert snapshot == "single line change"
            """
        ),
        "updated_5": (
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
        "updated_4": (
            """
            def test_updated_4(snapshot):
                assert snapshot == "sing line changeling"
            """
        ),
        "updated_5": (
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
    return {**testcases, **updated_testcases}


def test_missing_snapshots(testdir, testcases):
    testdir.makepyfile(test_file=testcases["used"])
    result = testdir.runpytest("-v")
    result.stdout.re_match_lines((r"1 snapshot failed\."))
    assert result.ret == 1


@pytest.fixture
def stubs(testdir, testcases):
    pyfile_content = "\n\n".join(testcases.values())
    testdir.makepyfile(test_file=pyfile_content)
    filepath = Path(testdir.tmpdir, "__snapshots__", "test_file.ambr")
    return testdir.runpytest("-v", "--snapshot-update"), testdir, testcases, filepath


def test_injected_fixture(stubs):
    result = stubs[0]
    result.stdout.fnmatch_lines(["*::test_injection PASSED*"])
    assert result.ret == 0


def test_generated_snapshots(stubs):
    result = stubs[0]
    result.stdout.re_match_lines((r"7 snapshots generated\."))
    assert result.ret == 0


def test_failing_snapshots_diff(stubs, testcases_updated):
    testdir = stubs[1]
    testdir.makepyfile(test_file="\n\n".join(testcases_updated.values()))
    result = testdir.runpytest("-vv", "--snapshot-no-colors")
    result.stdout.re_match_lines(
        (
            r".*assert snapshot == \['this', 'will', 'not', 'match'\]",
            r".*AssertionError: assert \[- snapshot\] == \[\+ received\]",
            r".*    <class 'list'> \[",
            r".*     ...",
            r".*      'will',",
            r".*  -   'be',",
            r".*  -   'updated',",
            r".*  \+   'not',",
            r".*  \+   'match',",
            r".*    \]",
            r".*assert \['this', 'will', 'fail'\] == snapshot",
            r".*AssertionError: assert \[\+ received\] == \[- snapshot\]",
            r".*    <class 'list'> \[",
            r".*     ...",
            r".*      'will',",
            r".*  -   'be',",
            r".*  \+   'fail',",
            r".*  -   'updated',",
            r".*    \]",
            r".*assert snapshot == \['this', 'will', 'be', 'too', 'much'\]",
            r".*AssertionError: assert \[- snapshot\] == \[\+ received\]",
            r".*    <class 'list'> \[",
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


def test_updated_snapshots(stubs, testcases_updated):
    testdir = stubs[1]
    testdir.makepyfile(test_file="\n\n".join(testcases_updated.values()))
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"2 snapshots passed\. 5 snapshots updated\."))
    assert result.ret == 0


def test_unused_snapshots(stubs):
    _, testdir, tests, _ = stubs
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v")
    result.stdout.re_match_lines(
        (
            r"6 snapshots passed\. 1 snapshot unused\.",
            r"Re-run pytest with --snapshot-update to delete unused snapshots\.",
        )
    )
    assert result.ret == 1


def test_unused_snapshots_warning(stubs):
    _, testdir, tests, _ = stubs
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v", "--snapshot-warn-unused")
    result.stdout.re_match_lines(
        (
            r"6 snapshots passed\. 1 snapshot unused\.",
            r"Re-run pytest with --snapshot-update to delete unused snapshots\.",
        )
    )
    assert result.ret == 0


def test_unused_snapshots_ignored_if_not_targeted_by_testnode_ids(testdir):
    path_to_snap = Path("__snapshots__", "other_snapfile")
    testdir.makefile(".ambr", **{str(path_to_snap): ""})
    testdir.makefile(
        ".py",
        test_life_uhh_finds_a_way=(
            """
            def test_life_always_finds_a_way(snapshot):
                assert snapshot == snapshot

            def test_clever_girl(snapshot):
                assert snapshot == snapshot
            """
        ),
    )
    testfile = Path(testdir.tmpdir, "test_life_uhh_finds_a_way.py")
    testdir.runpytest(str(testfile), "-v", "--snapshot-update")
    result = testdir.runpytest(
        f"{testfile}::test_life_always_finds_a_way", "-v", "--snapshot-update"
    )
    result.stdout.re_match_lines((r"1 snapshot passed\."))
    assert result.ret == 0
    assert Path(f"{path_to_snap}.ambr").exists()


def test_unused_snapshots_ignored_if_not_targeted_by_module_testfiles(stubs):
    _, testdir, tests, _ = stubs
    path_to_snap = Path("__snapshots__", "other_snapfile")
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    testdir.makefile(".ambr", **{str(path_to_snap): ""})
    result = testdir.runpytest("-v", "--snapshot-update", "test_file.py")
    result.stdout.re_match_lines(
        (
            r"6 snapshots passed\. 1 unused snapshot deleted\.",
            r"Deleted test_unused \(__snapshots__[\\/]test_file\.ambr\)",
        )
    )
    assert result.ret == 0
    assert Path(f"{path_to_snap}.ambr").exists()


def test_unused_snapshots_cleaned_up_when_targeting_specific_testfiles(stubs):
    _, testdir, _, _ = stubs
    path_to_snap = Path("__snapshots__", "other_snapfile")
    testdir.makepyfile(
        test_file=(
            """
            def test_used(snapshot):
                assert True
            """
        ),
    )
    testdir.makefile(".ambr", **{str(path_to_snap): ""})
    result = testdir.runpytest("-v", "--snapshot-update", "test_file.py")
    result.stdout.re_match_lines_random(
        (
            r"7 unused snapshots deleted\.",
            r"Deleted test_unused, test_updated_1, test_updated_2, test_updated_3",
            r".*test_updated_3, test_updated_4, test_updated_5, test_used",
            r".*test_used \(__snapshots__[\\/]test_file.ambr\)",
        )
    )
    assert result.ret == 0
    assert Path(f"{path_to_snap}.ambr").exists()


def test_removed_snapshots(stubs):
    _, testdir, tests, filepath = stubs
    assert Path(filepath).exists()
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines(
        (
            r"6 snapshots passed\. 1 unused snapshot deleted\.",
            r"Deleted test_unused \(__snapshots__[\\/]test_file\.ambr\)",
        )
    )
    assert result.ret == 0
    assert Path(filepath).exists()


def test_removed_snapshot_fossil(stubs):
    _, testdir, tests, filepath = stubs
    assert Path(filepath).exists()
    testdir.makepyfile(test_file=tests["inject"])
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines_random(
        (
            r"7 unused snapshots deleted\.",
            r"Deleted test_unused, test_updated_1, test_updated_2, test_updated_3",
            r".*test_updated_3, test_updated_4, test_updated_5, test_used",
            r".*test_used \(__snapshots__[\\/]test_file\.ambr\)",
        )
    )
    assert result.ret == 0
    assert not Path(filepath).exists()


def test_removed_empty_snapshot_fossil_only(stubs):
    _, testdir, _, filepath = stubs
    path_to_snap = Path("__snapshots__", "test_empty")
    testdir.makefile(".ambr", **{str(path_to_snap): ""})
    empty_filepath = Path(testdir.tmpdir, f"{path_to_snap}.ambr")
    assert empty_filepath.exists()
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines(
        (
            r"7 snapshots passed\. 1 unused snapshot deleted\.",
            r"Deleted empty snapshot fossil \(__snapshots__[\\/]test_empty\.ambr\)",
        )
    )
    assert result.ret == 0
    assert Path(filepath).exists()
    assert not Path(empty_filepath).exists()


def test_removed_hanging_snapshot_fossil(stubs):
    _, testdir, _, filepath = stubs
    path_to_snap = Path("__snapshots__", "test_hanging")
    testdir.makefile(".abc", **{str(path_to_snap): ""})
    hanging_filepath = Path(testdir.tmpdir, f"{path_to_snap}.abc")
    assert hanging_filepath.exists()
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = result.stdout.str()
    assert str(Path(filepath).relative_to(Path.cwd())) not in result_stdout
    assert "1 unused snapshot deleted" in result_stdout
    assert "unknown snapshot" in result_stdout
    assert str(hanging_filepath.relative_to(Path.cwd())) in result_stdout
    assert result.ret == 0
    assert Path(filepath).exists()
    assert not Path(hanging_filepath).exists()


def test_snapshot_default_extension_option(testdir):
    testdir.makepyfile(
        test_file=(
            """
            def test_default(snapshot):
                assert b"default extension serializer" == snapshot
            """
        ),
    )
    result = testdir.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-default-extension",
        "syrupy.extensions.single_file.SingleFileSnapshotExtension",
    )
    result.stdout.re_match_lines((r"1 snapshot generated\."))
    assert Path(
        testdir.tmpdir, "__snapshots__", "test_file", "test_default.raw"
    ).exists()
    assert result.ret == 0


def test_snapshot_default_extension_option_failure(testdir, testcases):
    testdir.makepyfile(test_file=testcases["used"])
    result = testdir.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-default-extension",
        "syrupy.extensions.amber.DoesNotExistExtension",
    )
    result_stderr = result.stderr.str()
    assert "error: argument --snapshot-default-extension" in result_stderr
    assert "Member 'DoesNotExistExtension' not found" in result_stderr
    assert result.ret
