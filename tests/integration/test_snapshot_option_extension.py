from pathlib import Path

import pytest


@pytest.fixture
def testfile(testdir):
    testdir.makepyfile(
        test_file=(
            """
            def test_default(snapshot):
                assert b"default extension serializer" == snapshot
            """
        ),
    )
    return testdir


def test_snapshot_default_extension_option_success(testfile):
    result = testfile.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-default-extension",
        "syrupy.extensions.single_file.SingleFileSnapshotExtension",
    )
    result_stdout = result.stdout.str()
    assert "1 snapshot generated." in result_stdout
    assert Path(
        testfile.tmpdir, "__snapshots__", "test_file", "test_default.raw"
    ).exists()
    assert not result.ret


def test_snapshot_default_extension_option_failure(testfile):
    result = testfile.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-default-extension",
        "syrupy.extensions.amber.DoesNotExistExtension",
    )
    result_stderr = result.stderr.str()
    assert "error: argument --snapshot-default-extension" in result_stderr
    assert "Member 'DoesNotExistExtension' not found" in result_stderr
    assert not Path(
        testfile.tmpdir, "__snapshots__", "test_file", "test_default.raw"
    ).exists()
    assert result.ret
