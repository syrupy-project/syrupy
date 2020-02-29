from pathlib import Path

import pytest

from .utils import clean_output


@pytest.fixture
def collection(testdir):
    tests = {
        "test_collected": (
            """
            import pytest

            @pytest.mark.collected
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
    result_stdout = clean_output(result.stdout.str())
    assert "4 snapshots generated" in result_stdout
    testdir.makefile(".ambr", **{"__snapshots__/other_snapfile": ""})
    return testdir


def test_unused_snapshots_ignored_if_not_targeted_using_dash_m(collection):
    updated_tests = {
        "test_collected": (
            """
            import pytest

            @pytest.mark.collected
            @pytest.mark.parametrize("actual", [1, "2"])
            def test_collected(snapshot, actual):
                assert snapshot == actual
            """
        ),
    }
    collection.makepyfile(**updated_tests)
    result = collection.runpytest("-v", "--snapshot-update", "-m", "collected")
    result_stdout = clean_output(result.stdout.str())
    assert "1 snapshot passed" in result_stdout
    assert "1 snapshot updated" in result_stdout
    assert "1 unused snapshot deleted" in result_stdout
    snapshot_path = [collection.tmpdir, "__snapshots__"]
    assert Path(*snapshot_path).joinpath("test_not_collected.ambr").exists()
    assert Path(*snapshot_path).joinpath("other_snapfile.ambr").exists()


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
    result_stdout = clean_output(result.stdout.str())
    assert "1 snapshot passed" in result_stdout
    assert "1 snapshot updated" in result_stdout
    assert "1 unused snapshot deleted" in result_stdout
    snapshot_path = [collection.tmpdir, "__snapshots__"]
    assert Path(*snapshot_path).joinpath("test_not_collected.ambr").exists()
    assert Path(*snapshot_path).joinpath("other_snapfile.ambr").exists()


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
    result_stdout = clean_output(result.stdout.str())
    assert "2 snapshots passed" in result_stdout
    assert "snapshot updated" not in result_stdout
    assert "1 unused snapshot deleted" in result_stdout
    snapshot_path = [collection.tmpdir, "__snapshots__"]
    assert Path(*snapshot_path).joinpath("test_not_collected.ambr").exists()
    assert Path(*snapshot_path).joinpath("other_snapfile.ambr").exists()


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
    assert "Snapshot does not exist" in clean_output(result.stdout.str())
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
    result_stdout = clean_output(result.stdout.str())
    assert "7 snapshots generated" in result_stdout
    assert "snapshots unused" not in result_stdout
    assert result.ret == 0


def test_failing_snapshots_diff(stubs, testcases_updated, snapshot):
    testdir = stubs[1]
    testdir.makepyfile(test_file="\n\n".join(testcases_updated.values()))
    result = testdir.runpytest("-vv")
    result_stdout = clean_output(result.stdout.str())
    start_index = result_stdout.find("==== FAILURES")
    end_index = result_stdout.find("==== 5 failed")
    result_stdout = "\n".join(
        line
        for line in result_stdout[start_index:end_index].splitlines()
        if not line.startswith("____") and not line.startswith("====")
    )
    assert snapshot == result_stdout
    assert result.ret == 1


def test_updated_snapshots(stubs, testcases_updated):
    testdir = stubs[1]
    testdir.makepyfile(test_file="\n\n".join(testcases_updated.values()))
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert "2 snapshots passed" in result_stdout
    assert "5 snapshots updated" in result_stdout
    assert result.ret == 0


def test_unused_snapshots(stubs):
    _, testdir, tests, _ = stubs
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v")
    result_stdout = clean_output(result.stdout.str())
    assert "snapshots generated" not in result_stdout
    assert "6 snapshots passed" in result_stdout
    assert "1 snapshot unused" in result_stdout
    assert result.ret == 1


def test_unused_snapshots_warning(stubs):
    _, testdir, tests, _ = stubs
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v", "--snapshot-warn-unused")
    result_stdout = clean_output(result.stdout.str())
    assert "snapshots generated" not in result_stdout
    assert "6 snapshots passed" in result_stdout
    assert "1 snapshot unused" in result_stdout
    assert result.ret == 0


def test_unused_snapshots_ignored_if_not_targeted_by_testnode_ids(stubs):
    _, testdir, tests, snapshot_file = stubs
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    testdir.makefile(
        ".ambr", **{"__snapshots__/other_snapfile": ""},
    )
    test_content = (
        "def test_life_always_finds_a_way(snapshot):\n\tassert snapshot == snapshot"
    )
    testdir.makefile(
        ".py", **{"test_life_always_finds_a_way": test_content},
    )
    testfile = Path(testdir.tmpdir, "test_life_always_finds_a_way.py")
    result = testdir.runpytest(
        f"{testfile}::test_life_always_finds_a_way", "-v", "--snapshot-update"
    )
    result_stdout = clean_output(result.stdout.str())
    assert "1 snapshot generated" in result_stdout
    assert result.ret == 0
    assert Path(snapshot_file).exists()
    assert Path("__snapshots__/other_snapfile.ambr").exists()


def test_unused_snapshots_ignored_if_not_targeted_by_module_testfiles(stubs):
    _, testdir, tests, _ = stubs
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    testdir.makefile(
        ".ambr", **{"__snapshots__/other_snapfile": ""},
    )
    result = testdir.runpytest("-v", "--snapshot-update", "test_file.py")
    result_stdout = clean_output(result.stdout.str())
    assert "1 unused snapshot deleted" in result_stdout
    assert result.ret == 0
    assert Path("__snapshots__/other_snapfile.ambr").exists()


def test_unused_snapshots_cleaned_up_when_targeting_specific_testfiles(stubs):
    _, testdir, tests, _ = stubs
    testdir.makepyfile(
        test_file=(
            """
            def test_used(snapshot):
                assert True
            """
        )
    )
    testdir.makefile(
        ".ambr", **{"__snapshots__/other_snapfile": ""},
    )
    result = testdir.runpytest("-v", "--snapshot-update", "test_file.py")
    result_stdout = clean_output(result.stdout.str())
    assert "7 unused snapshots deleted" in result_stdout
    assert result.ret == 0
    assert Path("__snapshots__/other_snapfile.ambr").exists()


def test_removed_snapshots(stubs):
    _, testdir, tests, filepath = stubs
    assert Path(filepath).exists()
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert "snapshot unused" not in result_stdout
    assert "1 unused snapshot deleted" in result_stdout
    assert result.ret == 0
    assert Path(filepath).exists()


def test_removed_snapshot_fossil(stubs):
    _, testdir, tests, filepath = stubs
    assert Path(filepath).exists()
    testdir.makepyfile(test_file=tests["inject"])
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert "snapshots unused" not in result_stdout
    assert "7 unused snapshots deleted" in result_stdout
    assert result.ret == 0
    assert not Path(filepath).exists()


def test_removed_empty_snapshot_fossil_only(stubs):
    _, testdir, _, filepath = stubs
    testdir.makefile(".ambr", **{"__snapshots__/test_empty": ""})
    empty_filepath = Path(testdir.tmpdir, "__snapshots__/test_empty.ambr")
    assert empty_filepath.exists()
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert str(Path(filepath).relative_to(Path.cwd())) not in result_stdout
    assert "1 unused snapshot deleted" in result_stdout
    assert "empty snapshot" in result_stdout
    assert str(empty_filepath.relative_to(Path.cwd())) in result_stdout
    assert result.ret == 0
    assert Path(filepath).exists()
    assert not Path(empty_filepath).exists()


def test_removed_hanging_snapshot_fossil(stubs):
    _, testdir, _, filepath = stubs
    testdir.makefile(".abc", **{"__snapshots__/test_hanging": ""})
    hanging_filepath = Path(testdir.tmpdir, "__snapshots__/test_hanging.abc")
    assert hanging_filepath.exists()
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert str(Path(filepath).relative_to(Path.cwd())) not in result_stdout
    assert "1 unused snapshot deleted" in result_stdout
    assert "unknown snapshot" in result_stdout
    assert str(hanging_filepath.relative_to(Path.cwd())) in result_stdout
    assert result.ret == 0
    assert Path(filepath).exists()
    assert not Path(hanging_filepath).exists()
