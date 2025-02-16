from pathlib import Path


def test_ignore_file_extensions(testdir):
    # Generate initial snapshot file
    testdir.makepyfile(
        test_file=(
            """
            def test_case(snapshot):
                assert snapshot == "some-value"
            """
        ),
    )
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"1 snapshot generated\.",))
    assert result.ret == 0

    # Duplicate the snapshot file with "dvc" file extension
    snapshot_file = Path(testdir.tmpdir, "__snapshots__", "test_file.ambr")
    dvc_file = snapshot_file.with_suffix(".ambr.dvc")
    dvc_file.write_text(snapshot_file.read_text())

    # Run with ignored file extension
    result = testdir.runpytest(
        "-v", "--snapshot-details", "--snapshot-ignore-file-extensions=dvc"
    )
    result.stdout.no_re_match_line(r".*1 snapshot unused.*")
