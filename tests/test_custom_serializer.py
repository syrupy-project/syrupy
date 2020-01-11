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

            def _discover_snapshots(self, snapshot_location):
                pass

            def get_snapshot_name(self, index = 0):
                testname = self._test_location.testname[::-1]
                return f"{testname}.{index}"

            def _read_snapshot_from_file(self, file, name):
                pass

            def _write_snapshot_to_file(self, snapshot_cache):
                pass

            def delete_snapshots_from_file(self, file, names):
                pass


        @pytest.fixture
        def snapshot_custom(snapshot):
            return snapshot.with_class(extension_class=CustomSnapshotExtension)
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
    assert "test_passed_custom" in result_stdout
    assert result.ret == 0
