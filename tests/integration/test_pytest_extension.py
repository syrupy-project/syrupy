import pytest

pytest_version = tuple(int(v) for v in pytest.__version__.split("."))


@pytest.fixture
def run_testcases(testdir):
    conftest = """
        import pytest

        class CustomItem(pytest.Item, pytest.File):
            def __init__(self, *args, fspath, parent, **kwargs):
                super().__init__(fspath, parent=parent)
                self._nodeid += "::CUSTOM"

            def runtest(self):
                pass

        def pytest_collect_file(path, parent):
            return CustomItem.from_parent(fspath=path, parent=parent)
        """
    testcase = """
        def test_example(snapshot):
            assert snapshot == 1
        """
    testdir.makepyfile(conftest=conftest)
    testdir.makepyfile(test_file=testcase)
    return testdir


@pytest.mark.skipif(pytest_version < (6, 0), reason="at least pytest 6 required")
def test_ignores_non_function_nodes(run_testcases):
    testdir = run_testcases
    result = testdir.runpytest("test_file.py", "-v", "--snapshot-update")
    result.stdout.re_match_lines((r".*test_file.py::CUSTOM.*"))
    assert result.ret == 0


def test_handles_pyargs_non_module_when_both_given(run_testcases):
    result = run_testcases.runpytest(
        "-v", "test_file.py", "--pyargs", "test_file", "--snapshot-update"
    )
    assert result.ret == 0
