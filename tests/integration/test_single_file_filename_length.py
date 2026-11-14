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

    snapshot_dir = Path(test_file).parent / "__snapshots__" / "test_file"
    snapshots = list(snapshot_dir.iterdir())
    assert len(snapshots) == 1
    assert len(snapshots[0].name) == 255
    assert snapshots[0].read_bytes() == b"expected_data"

    result = pytester.runpytest("-q")
    result.assert_outcomes(passed=1)
    assert result.ret == 0
