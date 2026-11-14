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


def test_extensionless_does_not_claim_sibling_extensions(pytester):
    """
    Empty file_extension must not treat other single-file snapshots as unused.

    ``str.endswith("")`` matches every path; without a tighter ownership check,
    directory-scoped discovery claims ``.json`` / ``.raw`` siblings and
    ``--snapshot-update`` deletes them.
    """
    test_file = pytester.makepyfile(
        test_file="""
        import pytest
        from syrupy.extensions.json import JSONSnapshotExtension
        from syrupy.extensions.single_file import SingleFileSnapshotExtension

        class Extensionless(SingleFileSnapshotExtension):
            file_extension = ""

        @pytest.fixture
        def snapshot_ext(snapshot):
            return snapshot.use_extension(Extensionless)

        @pytest.fixture
        def snapshot_json(snapshot):
            return snapshot.use_extension(JSONSnapshotExtension)

        class TestExample:
            def test_extensionless(self, snapshot_ext):
                assert b"extensionless" == snapshot_ext

            def test_json(self, snapshot_json):
                assert {"ok": True} == snapshot_json
        """
    )

    result = pytester.runpytest("--snapshot-update", "-q")
    result.assert_outcomes(passed=2)
    assert result.ret == 0

    snapshot_dir = Path(test_file).parent / "__snapshots__" / "test_file"
    extensionless = snapshot_dir / "TestExample.test_extensionless"
    json_snapshot = snapshot_dir / "TestExample.test_json.json"
    assert extensionless.read_bytes() == b"extensionless"
    assert json_snapshot.is_file()

    result = pytester.runpytest("--snapshot-update", "-q")
    result.assert_outcomes(passed=2)
    assert result.ret == 0
    assert "unused" not in result.stdout.str()
    assert extensionless.is_file()
    assert json_snapshot.is_file()
    assert json_snapshot.read_text(encoding="utf-8")
