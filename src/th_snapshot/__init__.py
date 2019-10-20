import pytest

from .assertion import SnapshotAssertion
from .io import SnapshotIO
from .serializer import SnapshotSerializer


def pytest_addoption(parser):
    group = parser.getgroup("th_snapshot")
    group.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        dest="update_snapshots",
        help="Update snapshots",
    )


@pytest.fixture
def snapshot(request):
    return SnapshotAssertion(
        update_snapshots=request.config.option.update_snapshots,
        io_class=SnapshotIO,
        serializer_class=SnapshotSerializer,
        test_filename=request.fspath,
        test_modulename=request.module.__name__,
        test_classname=request.cls.__name__ if request.cls else None,
        test_methodname=request.function.__name__ if request.function else None,
        test_nodename=getattr(request.node, "name", ""),
    )
