import argparse
import contextlib
import sys
from collections.abc import Iterator
from functools import lru_cache
from gettext import gettext
from typing import (
    Any,
    Optional,
)

import pytest

from syrupy.extensions.base import SnapshotCollectionStorage

from .assertion import DiffMode, SnapshotAssertion
from .constants import DISABLE_COLOR_ENV_VAR
from .exceptions import FailedToLoadModuleMember
from .extensions import DEFAULT_EXTENSION
from .location import PyTestLocation
from .patches.pycharm_diff import patch_pycharm_diff
from .session import SnapshotSession
from .terminal import (
    received_style,
    reset,
    snapshot_style,
)
from .utils import (
    env_context,
    import_module_member,
    is_xdist_worker,
)

# Global to have access to the session in `pytest_runtest_logfinish` hook
_syrupy: Optional["SnapshotSession"] = None


@lru_cache(maxsize=1)
def __import_extension(value: str | None) -> Any:
    if not value:
        return DEFAULT_EXTENSION
    try:
        return import_module_member(value)
    except FailedToLoadModuleMember as e:
        raise argparse.ArgumentTypeError(e) from e


def pytest_addoption(parser: "pytest.Parser") -> None:
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

    # We lazy evaluate the default extension since pytest-xdist requires
    # all pytest options to be serializable.
    group.addoption(
        "--snapshot-default-extension",
        default=None,
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
    group.addoption(
        "--snapshot-patch-pycharm-diff",
        action="store_true",
        default=False,
        dest="patch_pycharm_diff",
        help="Patch PyCharm diff",
    )
    group.addoption(
        "--snapshot-diff-mode",
        default=DiffMode.DETAILED,
        choices=list(DiffMode),
        type=DiffMode,
        dest="diff_mode",
        help="Controls how diffs are represented on snapshot assertion failure",
    )
    group.addoption(
        "--snapshot-ignore-file-extensions",
        dest="ignore_file_extensions",
        help="Comma separated list of file extensions to ignore when discovering snapshots",
        type=lambda v: v.split(","),
    )
    group.addoption(
        "--snapshot-dirname",
        dest="snapshot_dirname",
        default="__snapshots__",
        help="Directory name to use to store snapshots",
    )


def __terminal_color(
    config: "pytest.Config",
) -> "contextlib.AbstractContextManager[None]":
    if config.option.no_colors:
        env = {
            DISABLE_COLOR_ENV_VAR: "true",
        }
        return env_context(**env)
    else:
        # No-op to avoid unnecessary env updates
        return contextlib.nullcontext()


@pytest.hookimpl(tryfirst=True)
def pytest_assertrepr_compare(
    config: "pytest.Config", op: str, left: Any, right: Any
) -> list[str] | None:
    """
    Return explanation for comparisons in failing assert expressions.
    https://docs.pytest.org/en/latest/reference.html#pytest.hookspec.pytest_assertrepr_compare
    """
    if not isinstance(left, SnapshotAssertion) and not isinstance(
        right, SnapshotAssertion
    ):
        # Shortcut to minimise overhead in the case of other unrelated assertions
        return None

    with __terminal_color(config):
        received_name = received_style("[+ received]")

        def snapshot_name(name: str) -> str:
            return snapshot_style(f"[- {name}]")

        if isinstance(left, SnapshotAssertion):
            assert_msg = reset(f"{snapshot_name(left.name)} {op} {received_name}")
            return [assert_msg] + left.get_assert_diff(
                diff_mode=config.option.diff_mode
            )
        elif isinstance(right, SnapshotAssertion):
            assert_msg = reset(f"{received_name} {op} {snapshot_name(right.name)}")
            return [assert_msg] + right.get_assert_diff(
                diff_mode=config.option.diff_mode
            )
    return None


def pytest_sessionstart(session: Any) -> None:
    """
    Initialize snapshot session before tests are collected and ran.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionstart
    """

    # Override the snapshot dirname in the base SnapshotCollectionStorage class with the pytest config.
    SnapshotCollectionStorage.snapshot_dirname = session.config.option.snapshot_dirname

    session.config._syrupy = SnapshotSession(
        pytest_session=session,
        ignore_file_extensions=session.config.option.ignore_file_extensions,
    )
    global _syrupy
    _syrupy = session.config._syrupy
    session.config._syrupy.start()


def pytest_collection_modifyitems(
    session: Any, config: Any, items: list["pytest.Item"]
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


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """
    After each of the setup, call and teardown runtest phases of an item.
    https://docs.pytest.org/en/8.0.x/reference/reference.html#pytest.hookspec.pytest_runtest_logreport
    """
    global _syrupy
    # The outcome will be passed in the teardown phase even if skipped
    if _syrupy and report.when != "teardown":
        _syrupy.ran_item(report.nodeid, report.outcome)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session: "pytest.Session", exitstatus: int) -> None:
    """
    Finish session run and set exit status.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionfinish
    """
    session.exitstatus |= exitstatus | session.config._syrupy.finish()  # type: ignore[attr-defined]  # noqa: E501


def pytest_terminal_summary(
    terminalreporter: Any, exitstatus: int, config: Any
) -> None:
    """
    Add syrupy report to pytest.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_terminal_summary
    """
    if is_xdist_worker():
        # There is no need for pytest-xdist worker processes to generate a
        # summary and doing so has been seen to cause CPU spin and delays to
        # test run shutdown.
        return

    with __terminal_color(config):
        is_printing_report = False
        for line in terminalreporter.config._syrupy.report.lines:
            has_report_line = bool(line.strip())
            if has_report_line and not is_printing_report:
                terminalreporter.write_sep("-", gettext("snapshot report summary"))
                is_printing_report = True
            if is_printing_report:
                terminalreporter.write_line(line)


@pytest.fixture
def snapshot(request: "pytest.FixtureRequest") -> "SnapshotAssertion":
    return SnapshotAssertion(
        update_snapshots=request.config.option.update_snapshots,
        extension_class=__import_extension(request.config.option.default_extension),
        test_location=PyTestLocation(request.node),
        session=request.session.config._syrupy,  # type: ignore
    )


@pytest.fixture(scope="session", autouse=True)
def _syrupy_apply_ide_patches(request: "pytest.FixtureRequest") -> Iterator[None]:
    if request.config.option.patch_pycharm_diff:
        with patch_pycharm_diff():
            yield
    else:
        yield
