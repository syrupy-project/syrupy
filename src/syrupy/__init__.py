import argparse
import sys
from gettext import gettext
from typing import (
    Any,
    ContextManager,
    List,
    Optional,
)

import pytest

from .assertion import SnapshotAssertion
from .constants import DISABLE_COLOR_ENV_VAR
from .exceptions import FailedToLoadModuleMember
from .extensions import DEFAULT_EXTENSION
from .location import PyTestLocation
from .session import SnapshotSession
from .terminal import (
    received_style,
    reset,
    snapshot_style,
)
from .utils import (
    env_context,
    import_module_member,
)

# Global to have access to the session in `pytest_runtest_logfinish` hook
_syrupy: Optional["SnapshotSession"] = None


def __default_extension_option(value: str) -> Any:
    try:
        return import_module_member(value)
    except FailedToLoadModuleMember as e:
        raise argparse.ArgumentTypeError(e)


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
    group.addoption(
        "--snapshot-details",
        action="store_true",
        default=False,
        dest="include_snapshot_details",
        help="Include details of unused snapshots in the final report",
    )
    group.addoption(
        "--snapshot-default-extension",
        type=__default_extension_option,
        default=DEFAULT_EXTENSION,
        dest="default_extension",
        help="Specify the default snapshot extension",
    )
    group.addoption(
        "--snapshot-no-colors",
        action="store_true",
        default=not sys.stdout.isatty(),
        dest="no_colors",
        help="Disable test results output highlighting",
    )


def __terminal_color(config: Any) -> "ContextManager[None]":
    env = {}
    if config.option.no_colors:
        env[DISABLE_COLOR_ENV_VAR] = "true"

    return env_context(**env)


def pytest_assertrepr_compare(
    config: Any, op: str, left: Any, right: Any
) -> Optional[List[str]]:
    """
    Return explanation for comparisons in failing assert expressions.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_assertrepr_compare
    """
    with __terminal_color(config):
        received_name = received_style("[+ received]")

        def snapshot_name(name: str) -> str:
            return snapshot_style(f"[- {name}]")

        if isinstance(left, SnapshotAssertion):
            assert_msg = reset(f"{snapshot_name(left.name)} {op} {received_name}")
            return [assert_msg] + left.get_assert_diff()
        elif isinstance(right, SnapshotAssertion):
            assert_msg = reset(f"{received_name} {op} {snapshot_name(right.name)}")
            return [assert_msg] + right.get_assert_diff()
    return None


def pytest_sessionstart(session: Any) -> None:
    """
    Initialize snapshot session before tests are collected and ran.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionstart
    """
    session.config._syrupy = SnapshotSession(pytest_session=session)
    global _syrupy
    _syrupy = session.config._syrupy
    session.config._syrupy.start()


def pytest_collection_modifyitems(
    session: Any, config: Any, items: List["pytest.Item"]
) -> None:
    """
    After tests are collected and before any modification is performed.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_collection_modifyitems
    """
    config._syrupy.collect_items(items)


def pytest_collection_finish(session: Any) -> None:
    """
    After collection has been performed and modified.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_collection_finish
    """
    session.config._syrupy.select_items(session.items)


def pytest_runtest_logfinish(nodeid: str) -> None:
    """
    At the end of running the runtest protocol for a single item.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_runtest_logfinish
    """
    global _syrupy
    if _syrupy:
        _syrupy.ran_item(nodeid)


def pytest_sessionfinish(session: Any, exitstatus: int) -> None:
    """
    Finish session run and set exit status.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionfinish
    """
    session.exitstatus |= exitstatus | session.config._syrupy.finish()


def pytest_terminal_summary(
    terminalreporter: Any, exitstatus: int, config: Any
) -> None:
    """
    Add syrupy report to pytest.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_terminal_summary
    """
    with __terminal_color(config):
        terminalreporter.write_sep("-", gettext("snapshot report summary"))
        for line in terminalreporter.config._syrupy.report.lines:
            terminalreporter.write_line(line)


@pytest.fixture
def snapshot(request: Any) -> "SnapshotAssertion":
    return SnapshotAssertion(
        update_snapshots=request.config.option.update_snapshots,
        extension_class=request.config.option.default_extension,
        test_location=PyTestLocation(request.node),
        session=request.session.config._syrupy,
    )
