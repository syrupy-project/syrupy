"""Single-file extensions write immediately so large payloads are not buffered (#841)."""

from pathlib import Path

from syrupy.extensions.single_file import SingleFileSnapshotExtension


def test_single_file_writes_immediately(testdir) -> None:
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
        test_immediate="""
        def test_immediate(snapshot):
            assert b"payload" == snapshot
            # Mid-test: the snapshot file must already exist on disk.
            from pathlib import Path
            snaps = list(Path("__snapshots__").rglob("*.raw"))
            assert snaps, "expected single-file snapshot to be written immediately"
            assert snaps[0].read_bytes() == b"payload"
        """
    )
    result = testdir.runpytest("-v", "--snapshot-update")
    assert result.ret == 0
    result.stdout.re_match_lines((r"1 snapshot generated\.",))


def test_amber_still_buffers_until_session_end(testdir) -> None:
    testdir.makepyfile(
        test_buffered="""
        from pathlib import Path

        def test_buffered(snapshot):
            assert "payload" == snapshot
            snaps = list(Path("__snapshots__").rglob("*.ambr"))
            assert not snaps, "amber writes should remain buffered until session finish"
        """
    )
    result = testdir.runpytest("-v", "--snapshot-update")
    assert result.ret == 0
    assert (Path(testdir.tmpdir) / "__snapshots__" / "test_buffered.ambr").exists()


def test_write_immediately_flag_default() -> None:
    assert SingleFileSnapshotExtension.write_immediately is True
    from syrupy.extensions.amber import AmberSnapshotExtension

    assert AmberSnapshotExtension.write_immediately is False
