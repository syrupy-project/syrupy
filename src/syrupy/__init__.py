from typing import (
    Any,
    List,
    Optional,
)

import pytest

from .assertion import SnapshotAssertion
from .extensions import DEFAULT_EXTENSION
from .location import TestLocation
from .session import SnapshotSession
from .terminal import (
    green,
    red,
    reset,
)


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
    group.addoption(
        "--snapshot-warn-unused",
        action="store_true",
        default=False,
        dest="warn_unused_snapshots",
        help="Do not fail on unused snapshots",
    )


def pytest_assertrepr_compare(op: str, left: Any, right: Any) -> Optional[List[str]]:
    """
    Return explanation for comparisons in failing assert expressions.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_assertrepr_compare
    """
    if isinstance(left, SnapshotAssertion):
        assert_msg = reset(f"{green(left.name)} {op} {red('received')}")
        return [assert_msg] + left.get_assert_diff(right)
    elif isinstance(right, SnapshotAssertion):
        assert_msg = reset(f"{red('received')} {op} {green(right.name)}")
        return [assert_msg] + right.get_assert_diff(left)
    return None


def pytest_sessionstart(session: Any) -> None:
    """
    Initialize snapshot session before tests are collected and ran.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionstart
    """
    config = session.config
    session._syrupy = SnapshotSession(
        warn_unused_snapshots=config.option.warn_unused_snapshots,
        update_snapshots=config.option.update_snapshots,
        base_dir=config.rootdir,
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


def pytest_sessionfinish(session: Any, exitstatus: int) -> None:
    """
    Add syrupy report to pytest after whole test run finished, before exiting.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionfinish
    """
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    syrupy_exitstatus = session._syrupy.finish()
    for line in session._syrupy.report.lines:
        reporter.write_line(line)
    session.exitstatus |= syrupy_exitstatus


@pytest.fixture
def snapshot(request: Any) -> "SnapshotAssertion":
    return SnapshotAssertion(
        update_snapshots=request.config.option.update_snapshots,
        extension_class=DEFAULT_EXTENSION,
        test_location=TestLocation(request.node),
        session=request.session._syrupy,
    )
