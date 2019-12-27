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
    """
    Exposes snapshot plugin configuration to pytest.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_addoption
    """
    group = parser.getgroup("syrupy")
    group.addoption(
        "--snapshot-update",
        action="store_true",
        default=False,
        dest="update_snapshots",
        help="Update snapshots",
    )


def pytest_assertrepr_compare(op: str, left: Any, right: Any) -> Optional[List[str]]:
    """
    Return explanation for comparisons in failing assert expressions.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_assertrepr_compare
    """
    if isinstance(left, SnapshotAssertion):
        assert_msg = f"snapshot {op} {right}"
        return [assert_msg] + left.get_assert_diff(right)
    elif isinstance(right, SnapshotAssertion):
        assert_msg = f"{left} {op} snapshot"
        return [assert_msg] + right.get_assert_diff(left)
    return None


def pytest_sessionstart(session: Any) -> None:
    """
    Initialize snapshot session before tests are collected and ran.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionstart
    """
    config = session.config
    session._syrupy = SnapshotSession(
        update_snapshots=config.option.update_snapshots, base_dir=config.rootdir
    )
    session._syrupy.start()


def pytest_collection_modifyitems(session: Any, config: Any, items: List[Any]) -> None:
    """
    After tests are collected and before any modification is performed.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_collection_modifyitems
    """
    session._syrupy._all_items.update(items)


def pytest_collection_finish(session: Any) -> None:
    """
    After collection has been performed and modified.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_collection_finish
    """
    session._syrupy._ran_items.update(session.items)


def pytest_sessionfinish(session: Any) -> None:
    """
    Add syrupy report to pytest after whole test run finished, before exiting.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionfinish
    """
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
        testname=SnapshotSession.get_node_testname(request.node),
    )
    return SnapshotAssertion(
        update_snapshots=request.config.option.update_snapshots,
        serializer_class=DEFAULT_SERIALIZER,
        test_location=test_location,
        session=request.session._syrupy,
    )
