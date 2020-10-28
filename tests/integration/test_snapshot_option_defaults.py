import pytest


@pytest.fixture
def testcases():
    return {
        "inject": (
            """
            def test_injection(snapshot):
                assert snapshot is not None
            """
        ),
    }


@pytest.fixture
def run_testcases(testdir, testcases):
    pyfile_content = "\n\n".join(testcases.values())
    testdir.makepyfile(test_file=pyfile_content)
    return testdir.runpytest("-v")


def test_injected_fixture(run_testcases):
    run_testcases.stdout.fnmatch_lines(["*::test_injection PASSED*"])
    assert run_testcases.ret == 0
