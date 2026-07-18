import pytest


@pytest.fixture
def testcases():
    return {
        "used": (
            """
            def test_used(snapshot):
                assert snapshot == 'used'
            """
        ),
        "raise-skipped": (
            """
            import pytest
            def test_skipped(snapshot):
                pytest.skip("Skipping...")
                assert snapshot == 'unused'
            """
        ),
        "mark-skipped": (
            """
            import pytest
            @pytest.mark.skip
            def test_skipped(snapshot):
                assert snapshot == 'unused'
            """
        ),
        "not-skipped": (
            """
            def test_skipped(snapshot):
                assert snapshot == 'unused'
            """
        ),
    }


@pytest.fixture
def run_testcases(testdir, testcases):
    pyfile_content = "\n\n".join([testcases["used"], testcases["not-skipped"]])
    testdir.makepyfile(test_file=pyfile_content)
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines(r"2 snapshots generated\.")
    return testdir, testcases


def test_mark_skipped_snapshots(run_testcases, plugin_args):
    testdir, testcases = run_testcases
    pyfile_content = "\n\n".join([testcases["used"], testcases["mark-skipped"]])
    testdir.makepyfile(test_file=pyfile_content)

    result = testdir.runpytest("-v", *plugin_args)
    result.stdout.re_match_lines(r"1 snapshot passed\.$")
    assert result.ret == 0


def test_raise_skipped_snapshots(run_testcases, plugin_args):
    testdir, testcases = run_testcases
    pyfile_content = "\n\n".join([testcases["used"], testcases["raise-skipped"]])
    testdir.makepyfile(test_file=pyfile_content)

    result = testdir.runpytest("-v", *plugin_args)
    result.stdout.re_match_lines(r"1 snapshot passed\.$")
    assert result.ret == 0


def test_skipped_snapshots_update(run_testcases, plugin_args):
    testdir, testcases = run_testcases
    pyfile_content = "\n\n".join([testcases["used"], testcases["raise-skipped"]])
    testdir.makepyfile(test_file=pyfile_content)

    result = testdir.runpytest("-v", "--snapshot-update", *plugin_args)
    result.stdout.re_match_lines(r"1 snapshot passed\.$")
    assert result.ret == 0


def test_skipped_single_file_snapshot(testdir, plugin_args):
    testdir.makeconftest(
        """
        import pytest

        from syrupy.extensions.single_file import SingleFileSnapshotExtension

        @pytest.fixture
        def snapshot(snapshot):
            return snapshot.use_extension(SingleFileSnapshotExtension)
        """
    )
    testdir.makepyfile(
        """
        def test_used(snapshot):
            assert snapshot == b"used"

        def test_single_file(snapshot):
            assert snapshot == b"snapshot"
        """
    )
    result = testdir.runpytest("--snapshot-update")
    assert result.ret == 0

    testdir.makepyfile(
        """
        import pytest

        def test_used(snapshot):
            assert snapshot == b"used"

        @pytest.mark.skip
        def test_single_file(snapshot):
            assert snapshot == b"snapshot"
        """
    )
    result = testdir.runpytest(*plugin_args)

    assert "snapshot unused" not in result.stdout.str()
    assert result.ret == 0
