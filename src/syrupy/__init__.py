from typing import (
    Any,
    List,
    Optional,
)

import pytest

from .assertion import SnapshotAssertion
from .location import TestLocation
from .serializers import DEFAULT_SERIALIZER
from .session import SnapshotSession


def pytest_addoption(parser: Any) -> None:
    """Exposes snapshot plugin configuration to pytest."""
    group = parser.getgroup("syrupy")
    group.addoption(
        "--snapshot-update",
        action="store_true",
        default=False,
        dest="update_snapshots",
        help="Update snapshots",
    )


def pytest_assertrepr_compare(op: str, left: Any, right: Any) -> Optional[List[str]]:
    if isinstance(left, SnapshotAssertion):
        assert_msg = f"snapshot {op} {right}"
        return [assert_msg] + left.get_assert_diff(right)
    elif isinstance(right, SnapshotAssertion):
        assert_msg = f"{left} {op} snapshot"
        return [assert_msg] + right.get_assert_diff(left)
    return None


def pytest_sessionstart(session: Any) -> None:
    config = session.config
    session._syrupy = SnapshotSession(
        update_snapshots=config.option.update_snapshots, base_dir=config.rootdir
    )
    session._syrupy.start()


def pytest_sessionfinish(session: Any) -> None:
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    session._syrupy.finish()
    for line in session._syrupy.report:
        reporter.write_line(line)


@pytest.fixture
def snapshot(request: Any) -> "SnapshotAssertion":
    test_location = TestLocation(
        filename=request.fspath,
        modulename=request.module.__name__,
        classname=request.cls.__name__ if request.cls else None,
        methodname=request.function.__name__ if request.function else None,
        nodename=getattr(request.node, "name", ""),
        testname=getattr(
            request.node,
            "name",
            request.function.__name__ if request.function else None,
        ),
    )
    return SnapshotAssertion(
        update_snapshots=request.config.option.update_snapshots,
        serializer_class=DEFAULT_SERIALIZER,
        test_location=test_location,
        session=request.session._syrupy,
    )
