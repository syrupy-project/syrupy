import pytest

from syrupy.constants import DIFF_LINE_COUNT_LIMIT
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.extensions.base import SnapshotReporter


@pytest.mark.parametrize(
    "file_extension, location, expected",
    [
        ("json", "test.json", True),
        ("json", "test.custom.json", True),
        ("json", "test.ndjson", False),
        ("json", "testjson", False),
        ("json", "json", False),
        ("json", "test.json.bak", False),
        ("custom.raw", "test.custom.raw", True),
        ("custom.raw", "test.notcustom.raw", False),
        ("custom.raw", "testcustom.raw", False),
        ("custom.raw", "test.raw", False),
        ("", "test", True),
        ("", "TestClass.test_example", True),
        ("", "test.json", True),
    ],
)
def test_is_snapshot_location(file_extension, location, expected):
    extension = AmberSnapshotExtension()
    extension.file_extension = file_extension
    assert extension.is_snapshot_location(location=location) is expected


class SnapshotReporterNoContext(SnapshotReporter):
    @property
    def _context_line_count(self) -> int:
        return 0


@pytest.mark.parametrize("Reporter", [SnapshotReporter, SnapshotReporterNoContext])
class TestSnapshotReporter:
    @pytest.mark.parametrize(
        "a, b",
        [
            (
                "line 0\nline 1\nline 02\nline 3\nline 4\r\nline 5\nline 6\nline 7",
                "line 0\nline 1\nline 2\r\nline 3\nline 04\nline 5\nline 6\nline 7",
            ),
            (
                "line 0\nline 1\nline 2\nline 3\t\nline 4\nline 5\nline 6\nline 7",
                "line 0\nline 1\nline 2\nline 3  \nline 4\nline 5\nline 6\nline 7",
            ),
            (
                "line 0\nline 1\nline 2\nline 3\r\nline 4\nline 5\nline 6\nline 7",
                "line 0\rline 1\nline 2\r\nline 3\nline 4\nline 5\nline 6\nline 7",
            ),
        ],
        ids=lambda _: "",
    )
    def test_diff_lines(self, a, b, Reporter, snapshot, osenv):
        with osenv(NO_COLOR="true"):
            assert "\n".join(Reporter().diff_lines(a, b)) == snapshot

    def test_diff_large(self, Reporter, snapshot, osenv):
        n_count = 3000 + DIFF_LINE_COUNT_LIMIT * 2
        obj_a = [str(x) + ("a" * 20) for x in range(n_count)]
        obj_b = [
            line_a + ("b" if n > DIFF_LINE_COUNT_LIMIT else "")
            for n, line_a in enumerate(obj_a)
        ]
        str_a = "\n".join(obj_a)
        str_b = "\n".join(obj_b)
        with osenv(NO_COLOR="true"):
            assert "\n".join(Reporter().diff_lines(str_a, str_b)) == snapshot

    def test_diff_large_lines(self, Reporter, snapshot, osenv):
        n_count = 1000000
        obj_a = [str(x) + ("a" * n_count) for x in range(20)]
        obj_b = [line_a[: n_count // 2] + "b" * n_count for line_a in obj_a]
        str_a = "\n".join(obj_a)
        str_b = "\n".join(obj_b)
        with osenv(NO_COLOR="true"):
            assert "\n".join(Reporter().diff_lines(str_a, str_b)) == snapshot
