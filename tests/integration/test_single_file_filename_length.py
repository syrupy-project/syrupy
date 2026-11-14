from pathlib import Path

import pytest


@pytest.mark.parametrize("file_extension", ["raw", "custom.raw"])
def test_long_single_file_snapshot_name(pytester, file_extension):
    test_file = pytester.makepyfile(
        test_file=f"""
        import pytest
        from syrupy.extensions.single_file import SingleFileSnapshotExtension

        class CustomExtension(SingleFileSnapshotExtension):
            file_extension = {file_extension!r}

        @pytest.fixture
        def snapshot(snapshot):
            return snapshot.use_extension(CustomExtension)

        @pytest.mark.parametrize("value", [b"expected_data"], ids=["a" * 300])
        def test_long_name(value, snapshot):
            assert value == snapshot
        """
    )

    result = pytester.runpytest("--snapshot-update", "-q")
    result.assert_outcomes(passed=1)
    assert result.ret == 0
    output = result.stdout.str() + result.stderr.str()
    assert "Can not relate snapshot" not in output
    assert "unused" not in output

    snapshot_dir = Path(test_file).parent / "__snapshots__" / "test_file"
    snapshots = list(snapshot_dir.iterdir())
    assert len(snapshots) == 1
    assert len(snapshots[0].name) == 255
    assert snapshots[0].name.endswith(f".{file_extension}")
    assert snapshots[0].read_bytes() == b"expected_data"

    result = pytester.runpytest("-q")
    result.assert_outcomes(passed=1)
    assert result.ret == 0
    output = result.stdout.str() + result.stderr.str()
    assert "unused" not in output
    assert snapshots[0].exists()


@pytest.mark.parametrize("file_extension", ["raw", "custom.raw"])
def test_skipped_long_single_file_snapshot_is_kept(pytester, file_extension):
    """A truncated snapshot stays attributed to a skipped parametrized test."""
    test_file = pytester.makepyfile(
        test_file=f"""
        from pathlib import Path

        import pytest
        from syrupy.extensions.single_file import SingleFileSnapshotExtension

        class CustomExtension(SingleFileSnapshotExtension):
            file_extension = {file_extension!r}

        @pytest.fixture
        def snapshot(snapshot):
            return snapshot.use_extension(CustomExtension)

        @pytest.mark.skipif(
            Path(__file__).with_name("skip_long").exists(),
            reason="hold the generated snapshot",
        )
        @pytest.mark.parametrize("value", [b"expected_data"], ids=["a" * 300])
        def test_long_name(value, snapshot):
            assert value == snapshot

        def test_short(snapshot):
            assert b"other" == snapshot
        """
    )

    result = pytester.runpytest("--snapshot-update", "-q")
    result.assert_outcomes(passed=2)
    assert result.ret == 0

    snapshot_dir = Path(test_file).parent / "__snapshots__" / "test_file"
    long_snapshot = next(
        path for path in snapshot_dir.iterdir() if len(path.name) == 255
    )
    assert long_snapshot.name.endswith(f".{file_extension}")
    assert long_snapshot.read_bytes() == b"expected_data"

    Path(test_file).with_name("skip_long").write_text("")

    result = pytester.runpytest("-q")
    result.assert_outcomes(passed=1, skipped=1)
    assert result.ret == 0
    output = result.stdout.str() + result.stderr.str()
    assert "unused" not in output
    assert long_snapshot.exists()

    result = pytester.runpytest("--snapshot-update", "-q")
    result.assert_outcomes(passed=1, skipped=1)
    assert result.ret == 0
    output = result.stdout.str() + result.stderr.str()
    assert "unused" not in output
    assert long_snapshot.read_bytes() == b"expected_data"
