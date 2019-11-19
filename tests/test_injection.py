def test_fixture(testdir):
    testdir.makepyfile(
        """
        def test_sth(snapshot):
            assert snapshot is not None
    """
    )

    result = testdir.runpytest("-v")
    result.stdout.fnmatch_lines(["*::test_sth PASSED*"])

    assert result.ret == 0
