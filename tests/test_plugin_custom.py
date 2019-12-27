import pytest

from .utils import clean_output


@pytest.fixture
def testcases(testdir):
    testdir.makeconftest(
        """
        import pytest

        from syrupy.serializers.base import AbstractSnapshotSerializer

        class CustomSnapshotSerializer(AbstractSnapshotSerializer):
            def file_extension(self):
                return ""

            def serialize(self, data):
                return str(data)

            def discover_snapshots(self, filepath):
                return set()

            def get_snapshot_name(self, index = 0):
                methodname = self._test_location.testname[::-1]
                return f"{methodname}.{index}"

            def read_snapshot_from_file(self, snapshot_file, snapshot_name):
                pass

            def write_snapshot_or_remove_file(self, snapshot_file, snapshot_name, data):
                pass


        @pytest.fixture
        def snapshot_custom(snapshot):
            return snapshot.with_class(serializer_class=CustomSnapshotSerializer)
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
    assert "does not contain testname" in result_stdout
    assert result.ret == 0
