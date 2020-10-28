import pytest


@pytest.fixture
def testcases_initial(testdir):
    testdir.makeconftest(
        """
        import pytest

        from syrupy.extensions.amber import AmberSnapshotExtension
        from syrupy.extensions.image import (
            PNGImageSnapshotExtension,
            SVGImageSnapshotExtension,
        )
        from syrupy.extensions.single_file import SingleFileSnapshotExtension


        class CustomSnapshotExtension(AmberSnapshotExtension):
            @property
            def _file_extension(self):
                return ""

            def serialize(self, data, **kwargs):
                return str(data)

            def get_snapshot_name(self, *, index = 0):
                testname = self._test_location.testname[::-1]
                return f"{testname}.{index}"

            def _get_file_basename(self, *, index = 0):
                return self.test_location.filename[::-1]

        @pytest.fixture
        def snapshot_custom(snapshot):
            return snapshot.use_extension(CustomSnapshotExtension)


        @pytest.fixture
        def snapshot_single(snapshot):
            return snapshot.use_extension(SingleFileSnapshotExtension)


        @pytest.fixture
        def snapshot_png(snapshot):
            return snapshot.use_extension(PNGImageSnapshotExtension)


        @pytest.fixture
        def snapshot_svg(snapshot):
            return snapshot.use_extension(SVGImageSnapshotExtension)
        """
    )
    return {
        "passed": (
            """
            def test_passed_custom(snapshot_custom):
                assert snapshot_custom == 'passed1'
                assert snapshot_custom == 'passed2'

            def test_passed_single(snapshot_single):
                assert snapshot_single == b'passed1'
                assert snapshot_single == b'passed2'
            """
        ),
        "failed": (
            """
            def test_failed_single(snapshot_single):
                assert snapshot_single == 'failed'

            def test_failed_image(snapshot_png):
                assert "not a byte string" == snapshot_png
            """
        ),
    }


@pytest.fixture
def testcases_updated(testcases_initial):
    updated_testcases = {
        "passed": (
            """
            def test_passed_single(snapshot_single):
                assert snapshot_single == b'passed'
            """
        )
    }
    return {**testcases_initial, **updated_testcases}


@pytest.fixture
def generate_snapshots(testdir, testcases_initial):
    testdir.makepyfile(test_file=testcases_initial["passed"])
    result = testdir.runpytest("-v", "--snapshot-update")
    return result, testdir, testcases_initial


def test_unsaved_snapshots(testdir, testcases_initial):
    testdir.makepyfile(test_file=testcases_initial["passed"])
    result = testdir.runpytest("-v")
    output = result.stdout.str()
    assert "Snapshot 'test_passed_single' does not exist" in output
    assert "+ b'passed1'" in output
    assert result.ret == 1


def test_failed_snapshots(testdir, testcases_initial):
    testdir.makepyfile(test_file=testcases_initial["failed"])
    result = testdir.runpytest("-v", "--snapshot-update")
    assert "2 snapshots failed" in result.stdout.str()
    assert result.ret == 1


def test_generated_snapshots(generate_snapshots):
    result = generate_snapshots[0]
    result_stdout = result.stdout.str()
    assert "4 snapshots generated" in result_stdout
    assert "snapshots unused" not in result_stdout
    assert result.ret == 0


def test_unmatched_snapshots(generate_snapshots, testcases_updated):
    testdir = generate_snapshots[1]
    testdir.makepyfile(test_file=testcases_updated["passed"])
    result = testdir.runpytest("-v")
    result_stdout = result.stdout.str()
    assert "1 snapshot failed" in result_stdout
    assert "2 snapshots unused" in result_stdout
    assert result.ret == 1


def test_updated_snapshots(generate_snapshots, testcases_updated):
    testdir = generate_snapshots[1]
    testdir.makepyfile(test_file=testcases_updated["passed"])
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = result.stdout.str()
    assert "1 snapshot updated" in result_stdout
    assert "2 unused snapshots deleted" in result_stdout
    assert result.ret == 0


def test_warns_on_snapshot_name(generate_snapshots):
    result = generate_snapshots[0]
    result_stdout = result.stdout.str()
    assert "4 snapshots generated" in result_stdout
    assert "Warning:" in result_stdout
    assert "Can not relate snapshot name" in result_stdout
    assert "Can not relate snapshot location" in result_stdout
    assert "test_passed_custom" in result_stdout
    assert result.ret == 0
