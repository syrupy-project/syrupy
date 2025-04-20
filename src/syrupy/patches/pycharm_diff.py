import warnings
from collections.abc import Iterator
from contextlib import contextmanager
from functools import wraps
from inspect import signature
from typing import (
    Any,
)

from syrupy.assertion import SnapshotAssertion


@contextmanager
def patch_pycharm_diff() -> Iterator[None]:
    """
    Applies PyCharm diff patch to add Syrupy snapshot support.
    See: https://github.com/syrupy-project/syrupy/issues/675
    """

    try:
        from teamcity.diff_tools import EqualsAssertionError  # type: ignore
    except ImportError:
        warnings.warn(
            "Failed to patch PyCharm's diff tools. Skipping patch.",
            stacklevel=2,
        )
        yield
        return

    old_init = EqualsAssertionError.__init__
    old_init_signature = signature(old_init)

    @wraps(old_init)
    def new_init(self: "EqualsAssertionError", *args: Any, **kwargs: Any) -> None:
        # Extract the __init__ arguments as originally passed in order to
        # process them later
        parameters = old_init_signature.bind(self, *args, **kwargs)
        parameters.apply_defaults()

        expected = parameters.arguments["expected"]
        actual = parameters.arguments["actual"]
        real_exception = parameters.arguments["real_exception"]

        if isinstance(expected, SnapshotAssertion):
            snapshot = expected
        elif isinstance(actual, SnapshotAssertion):
            snapshot = actual
        else:
            snapshot = None

        old_init(self, *args, **kwargs)

        # No snapshot was involved in the assertion. Let the old logic do its
        # thing.
        if snapshot is None:
            return

        # Although a snapshot was involved in the assertion, it seems the error
        # was a result of a non-assertion exception (Ex. `assert 1/0`).
        # Therefore, We will not do anything here either.
        if real_exception is not None:
            return

        assertion_result = snapshot.executions[snapshot.num_executions - 1]
        if assertion_result.exception is not None:
            return

        self.expected = str(assertion_result.recalled_data)
        self.actual = str(assertion_result.asserted_data)

    try:
        EqualsAssertionError.__init__ = new_init
        yield
    finally:
        EqualsAssertionError.__init__ = old_init
