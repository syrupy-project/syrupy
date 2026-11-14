from pathlib import Path


def test_extensionless_single_file_snapshots(pytester):
    testcase = """
    import pytest
    from syrupy.extensions.single_file import SingleFileSnapshotExtension

    class Extensionless(SingleFileSnapshotExtension):
        file_extension = ""

    @pytest.fixture
    def snapshot(snapshot):
        return snapshot.use_extension(Extensionless)

    class TestExample:
        def test_value(self, snapshot):
            assert b"expected_data" == snapshot
    """
    test_file = pytester.makepyfile(test_file=testcase)

    result = pytester.runpytest("--snapshot-update", "-q")
    result.assert_outcomes(passed=1)
    assert result.ret == 0

    snapshot_file = (
        Path(test_file).parent
        / "__snapshots__"
        / "test_file"
        / "TestExample.test_value"
    )
    assert snapshot_file.read_bytes() == b"expected_data"

    result = pytester.runpytest("-q")
    result.assert_outcomes(passed=1)
    assert result.ret == 0

    pytester.makepyfile(test_file=testcase.replace("expected_data", "updated_data"))
    result = pytester.runpytest("--snapshot-update", "-q")
    result.assert_outcomes(passed=1)
    assert result.ret == 0
    assert snapshot_file.read_bytes() == b"updated_data"
