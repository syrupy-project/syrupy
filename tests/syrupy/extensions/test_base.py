import pytest

from syrupy.constants import DIFF_LINE_COUNT_LIMIT
from syrupy.extensions.base import SnapshotReporter


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

    def test_diff_large(self, Reporter, osenv):
        n_count = 3000 + DIFF_LINE_COUNT_LIMIT * 2
        obj_a = [str(x) + ("a" * 20) for x in range(n_count)]
        obj_b = [line_a + "b" for line_a in obj_a]
        str_a = "\n".join(obj_a)
        str_b = "\n".join(obj_b)
        with osenv(NO_COLOR="true"):
            assert (
                len(list(Reporter().diff_lines(str_a, str_b)))
                <= DIFF_LINE_COUNT_LIMIT * 2
            )

    def test_diff_large_lines(self, Reporter, osenv):
        n_count = 5000
        obj_a = [str(x) + ("a" * n_count) for x in range(20)]
        obj_b = [line_a[: n_count // 2] + "b" * n_count for line_a in obj_a]
        str_a = "\n".join(obj_a)
        str_b = "\n".join(obj_b)
        with osenv(NO_COLOR="true"):
            assert (
                len(list(Reporter().diff_lines(str_a, str_b)))
                <= DIFF_LINE_COUNT_LIMIT * 2
            )
