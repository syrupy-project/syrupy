import pytest

from .utils import clean_output


@pytest.fixture
def testcases(testdir):
    testdir.makeconftest(
        """
        import pytest

        from syrupy.extensions.base import AbstractSyrupyExtension

        class CustomSnapshotExtension(AbstractSyrupyExtension):
            def _file_extension(self):
                return ""

            def serialize(self, data):
                return str(data)

            def get_snapshot_name(self, *, index = 0):
                testname = self._test_location.testname[::-1]
                return f"{testname}.{index}"

            def _read_snapshot_fossil(self, **kwargs):
                pass

            def _read_snapshot_data_from_location(self, **kwargs):
                pass

            def _write_snapshot_fossil(self, **kwargs):
                pass

            def delete_snapshots(self, **kwargs):
                pass

            def _get_file_basename(self, *, index = 0):
                return self.test_location.filename[::-1]


        @pytest.fixture
        def snapshot_custom(snapshot):
            return snapshot.use_extension(CustomSnapshotExtension)
        """
    )
    return {
        "passed": (
            """
            def test_passed_custom(snapshot_custom):
                assert snapshot_custom == 'passed1'
                assert snapshot_custom == 'passed2'
            """
        )
    }


def test_warns_on_snapshot_name(testdir, testcases):
    testdir.makepyfile(test_file=testcases["passed"])
    result = testdir.runpytest("-v", "--snapshot-update")
    result_stdout = clean_output(result.stdout.str())
    assert "2 snapshots generated" in result_stdout
    assert "Warning:" in result_stdout
    assert "Can not relate snapshot name" in result_stdout
    assert "Can not relate snapshot location" in result_stdout
    assert "test_passed_custom" in result_stdout
    assert result.ret == 0
