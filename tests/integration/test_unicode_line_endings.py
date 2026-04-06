def test_can_correctly_snapshot_unicode_line_endings(testdir):
    testdir.makepyfile(
        test_file="""
        def test_snapshot_with_unicode_linesep(snapshot):
            assert "\\x1e\\n" == snapshot
        """
    )

    result = testdir.runpytest("--snapshot-update")
    assert result.ret == 0

    result = testdir.runpytest()
    assert result.ret == 0
