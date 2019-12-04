def test_fixture(testdir):
    pyfile_content = """
def test_sth(snapshot):
    assert snapshot is not None
"""
    testdir.makepyfile(pyfile_content)

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_sth PASSED*"])

    assert result.ret == 0
