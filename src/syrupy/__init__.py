import argparse
import glob
from gettext import gettext
from typing import (
    Any,
    List,
    Optional,
)

import pytest

from .assertion import SnapshotAssertion
from .exceptions import FailedToLoadModuleMember
from .extensions import DEFAULT_EXTENSION
from .location import TestLocation
from .session import SnapshotSession
from .terminal import (
    received_style,
    reset,
    snapshot_style,
)
from .utils import import_module_member


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
        "--snapshot-default-extension",
        type=__default_extension_option,
        default=DEFAULT_EXTENSION,
        dest="default_extension",
        help="Specify the default snapshot extension",
    )


def pytest_assertrepr_compare(op: str, left: Any, right: Any) -> Optional[List[str]]:
    """
    Return explanation for comparisons in failing assert expressions.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_assertrepr_compare
    """
    if isinstance(left, SnapshotAssertion):
        assert_msg = reset(
            f"{snapshot_style(left.name)} {op} {received_style('received')}"
        )
        return [assert_msg] + left.get_assert_diff(right)
    elif isinstance(right, SnapshotAssertion):
        assert_msg = reset(
            f"{received_style('received')} {op} {snapshot_style(right.name)}"
        )
        return [assert_msg] + right.get_assert_diff(left)
    return None


def __is_testpath(arg: str) -> bool:
    return not arg.startswith("-") and bool(glob.glob(arg.split("::")[0]))


def __is_testnode(arg: str) -> bool:
    return __is_testpath(arg) and "::" in arg


def __is_testmodule(arg: str) -> bool:
    return arg == "--pyargs"


def pytest_sessionstart(session: Any) -> None:
    """
    Initialize snapshot session before tests are collected and ran.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionstart
    """
    config = session.config
    config._syrupy = SnapshotSession(
        warn_unused_snapshots=config.option.warn_unused_snapshots,
        update_snapshots=config.option.update_snapshots,
        base_dir=config.rootdir,
        is_providing_paths=any(
            __is_testpath(arg) or __is_testmodule(arg)
            for arg in config.invocation_params.args
        ),
        is_providing_nodes=any(
            __is_testnode(arg) for arg in config.invocation_params.args
        ),
    )
    config._syrupy.start()


def pytest_collection_modifyitems(
    session: Any, config: Any, items: List["pytest.Item"]
) -> None:
    """
    After tests are collected and before any modification is performed.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_collection_modifyitems
    """
    for item in config._syrupy.filter_valid_items(items):
        config._syrupy._all_items[item] = True


def pytest_collection_finish(session: Any) -> None:
    """
    After collection has been performed and modified.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_collection_finish
    """
    for item in session.config._syrupy.filter_valid_items(session.items):
        session.config._syrupy._ran_items[item] = True


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
    terminalreporter.write_sep("-", gettext("snapshot report summary"))
    for line in terminalreporter.config._syrupy.report.lines:
        terminalreporter.write_line(line)


@pytest.fixture
def snapshot(request: Any) -> "SnapshotAssertion":
    return SnapshotAssertion(
        update_snapshots=request.config.option.update_snapshots,
        extension_class=request.config.option.default_extension,
        test_location=TestLocation(request.node),
        session=request.session.config._syrupy,
    )
