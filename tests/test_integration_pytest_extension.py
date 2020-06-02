from .utils import clean_output


def test_ignores_non_function_nodes(testdir):
    conftest = """
        import pytest

        class CustomItem(pytest.Item, pytest.File):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._nodeid += "::CUSTOM"

            def runtest(self):
                pass

        def pytest_collect_file(path, parent):
            return CustomItem(path, parent)
        """
    testcase = """
        def test_example(snapshot):
            assert snapshot == 1
        """
    testdir.makepyfile(conftest=conftest)
    testdir.makepyfile(test_file=testcase)
    result = testdir.runpytest("test_file.py", "-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert result.ret == 0
    assert "test_file.py::CUSTOM" in result_stdout
