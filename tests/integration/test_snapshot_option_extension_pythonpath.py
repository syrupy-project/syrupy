from pathlib import Path

import pytest


@pytest.fixture
def testfile(testdir):
    testdir.makepyfile(
        extension_file=(
            """
            import syrupy
            class MySingleFileExtension(
                syrupy.extensions.single_file.SingleFileSnapshotExtension
            ):
                pass
            """
        ),
        test_file=(
            """
            def test_default(snapshot):
                assert b"default extension serializer" == snapshot
            """
        ),
    )
    return testdir


def test_snapshot_default_extension_option_success(testfile):
    testfile.makeini(
        f"""
        [pytest]
        pythonpath =
            {testfile.tmpdir}
    """
    )

    result = testfile.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-default-extension",
        "extension_file.MySingleFileExtension",
    )
    result.stdout.re_match_lines((r"1 snapshot generated\."))
    assert Path(
        testfile.tmpdir, "__snapshots__", "test_file", "test_default.raw"
    ).exists()
    assert not result.ret


def test_snapshot_default_extension_option_module_not_found(testfile):
    result = testfile.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-default-extension",
        "extension_file.MySingleFileExtension",
    )
    result.stdout.re_match_lines((r".*: Module 'extension_file' does not exist.*",))
    assert not Path(
        testfile.tmpdir, "__snapshots__", "test_file", "test_default.raw"
    ).exists()
    assert result.ret


def test_snapshot_default_extension_option_failure(testfile):
    testfile.makeini(
        f"""
        [pytest]
        pythonpath =
            {testfile.tmpdir}
    """
    )

    result = testfile.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-default-extension",
        "extension_file.DoesNotExistExtension",
    )
    result.stdout.re_match_lines((r".*: Member 'DoesNotExistExtension' not found.*",))
    assert not Path(
        testfile.tmpdir, "__snapshots__", "test_file", "test_default.raw"
    ).exists()
    assert result.ret
