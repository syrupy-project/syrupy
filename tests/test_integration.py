import os

import pytest


@pytest.fixture
def stubs(testdir):
    tests = {
        "inject": """def test_injection(snapshot):
    assert snapshot is not None""",
        "used": """def test_used(snapshot):
    assert snapshot == 'used'""",
        "unused": """def test_unused(snapshot):
    assert snapshot == 'unused'""",
    }
    pyfile_content = "\n\n".join(tests.values())
    testdir.makepyfile(test_file=pyfile_content)
    filepath = os.path.join(testdir.tmpdir, "__snapshots__", "test_file.yaml")
    return testdir.runpytest("-v", "--snapshot-update"), testdir, tests, filepath


def test_fixture(stubs):
    result = stubs[0]
    result.stdout.fnmatch_lines(["*::test_injection PASSED*"])
    assert result.ret == 0


def test_generate_snapshots(stubs):
    result = stubs[0]
    assert "2\x1b[0m snapshots generated" in result.stdout.str()
    assert "0\x1b[0m snapshots unused" in result.stdout.str()
    assert result.ret == 0


def test_unused_snapshots(stubs):
    result, testdir, tests, _ = stubs
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v")
    assert "snapshots generated" not in result.stdout.str()
    assert "1\x1b[0m snapshot unused" in result.stdout.str()
    assert result.ret == 0


def test_removed_snapshots(stubs):
    _, testdir, tests, filepath = stubs
    assert os.path.isfile(filepath)
    testdir.makepyfile(test_file="\n\n".join(tests[k] for k in tests if k != "unused"))
    result = testdir.runpytest("-v", "--snapshot-update")
    assert "1\x1b[0m snapshot unused" in result.stdout.str()
    assert "This snapshot has been deleted" in result.stdout.str()
    assert result.ret == 0
    assert os.path.isfile(filepath)


def test_removed_snapshot_file(stubs):
    _, testdir, tests, filepath = stubs
    assert os.path.isfile(filepath)
    testdir.makepyfile(test_file=tests["inject"])
    result = testdir.runpytest("-v", "--snapshot-update")
    assert "2\x1b[0m snapshots unused" in result.stdout.str()
    assert "These snapshots have been deleted" in result.stdout.str()
    assert result.ret == 0
    assert not os.path.isfile(filepath)
