import pytest

from syrupy.extensions.base import SnapshotReporter

from .utils import clean_output


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
        ],
        ids=lambda _: "",
    )
    def test_diff_lines(self, a, b, Reporter, snapshot):
        assert "\n".join(map(clean_output, Reporter().diff_lines(a, b))) == snapshot
