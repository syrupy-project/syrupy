def test_raises_informative_type_error_when_serializing_non_bytes(testdir):
    testdir.makepyfile(
        test_file="""
        from syrupy.extensions.single_file import SingleFileSnapshotExtension

        def test_case(snapshot):
            assert {"x": 0} == snapshot(extension_class=SingleFileSnapshotExtension)
        """
    )

    result = testdir.runpytest("-v")
    assert result.ret == 1
    result.stdout.re_match_lines(
        (r".*TypeError: Can't serialize.*You must convert the data.*",)
    )
