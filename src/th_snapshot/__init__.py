import pytest

from .assertion import SnapshotAssertion
from .io import SnapshotIO
from .serializer import SnapshotSerializer
from .location import TestLocation


def pytest_addoption(parser):
    """Exposes snapshot plugin configuration to pytest."""
    group = parser.getgroup("th_snapshot")
    group.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        dest="update_snapshots",
        help="Update snapshots",
    )


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, SnapshotAssertion):
        assert_msg = f"snapshot {op} {right}"
        return [assert_msg] + left.get_assert_diff(right)
    elif isinstance(right, SnapshotAssertion):
        assert_msg = f"{left} {op} snapshot"
        return [assert_msg] + right.get_assert_diff(left)
    return None


@pytest.fixture
def snapshot(request):
    test_location = TestLocation(
        filename=request.fspath,
        modulename=request.module.__name__,
        classname=request.cls.__name__ if request.cls else None,
        methodname=request.function.__name__ if request.function else None,
        nodename=getattr(request.node, "name", ""),
        testname=getattr(request.node, "name", "")
        or (request.function.__name__ if request.function else None),
    )
    return SnapshotAssertion(
        update_snapshots=request.config.option.update_snapshots,
        io_class=SnapshotIO,
        serializer_class=SnapshotSerializer,
        test_location=test_location,
    )
