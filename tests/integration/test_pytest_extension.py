import pytest

pytest_version = tuple(int(v) for v in pytest.__version__.split("."))


@pytest.fixture
def run_testcases(testdir):
    conftest = """
        def pytest_itemcollected(item):
            item._nodeid += "::CUSTOM"
        """
    testcase = """
        def test_example(snapshot):
            assert snapshot == 1
        """
    testdir.makeconftest(conftest)
    testdir.makepyfile(test_file=testcase)
    return testdir


def test_ignores_non_function_nodes(run_testcases):
    testdir = run_testcases
    result = testdir.runpytest("test_file.py", "-v", "--snapshot-update")
    result.stdout.re_match_lines((r".*test_file.*::CUSTOM.*"))
    assert result.ret == 0


def test_handles_pyargs_non_module_when_both_given(run_testcases):
    result = run_testcases.runpytest(
        "-v", "test_file.py", "--pyargs", "test_file", "--snapshot-update"
    )
    assert result.ret == 0
