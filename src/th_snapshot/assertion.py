import traceback
import pytest
import os

from .exceptions import SnapshotDoesNotExist
from .terminal import error_style, bold


class SnapshotAssertion:
    _update_snapshots = None
    _io_class = None
    _serializer = None

    _test_filename = None
    _test_name = None

    _executions = 0

    def __init__(self, update_snapshots, io_class, serializer_class, **kwargs):
        self._update_snapshots = update_snapshots
        self._io_class = io_class(**kwargs)
        self._serializer = serializer_class()

        self._test_filename = kwargs.get("test_filename")
        self._test_name = kwargs.get("test_nodename") or kwargs.get("test_methodname")

    def __repr__(self):
        return f"<SnapshotAssertion ({self._executions})>"

    def _get_assertion(self):
        for fn, lineno, func, text in reversed(traceback.extract_stack()):
            if fn == self._test_filename:
                return dict(
                    filename=os.path.relpath(fn, os.getcwd()),
                    lineno=lineno,
                    function_name=func,
                    text=text,
                )
        return None

    def _fail(self, msg):
        indent = " " * 4
        lines = [""]

        assertion = self._get_assertion()
        if assertion:
            lines.extend(
                [
                    bold(f" {indent}def {self._test_name}(..."),
                    f">{indent * 2}{bold(assertion['text'])}",
                ]
            )

        lines.extend(f"{error_style('E')}{indent * 2}{m}" for m in msg)

        if assertion:
            lines.extend(
                [
                    "",
                    f"{error_style(assertion['filename'])}:{assertion['lineno']}: SnapshotError",
                ]
            )

        pytest.fail("\n".join(lines), False)
        return False

    def __call__(self, data):
        return self._assert(data)

    def _assert(self, data):
        executions = self._executions
        self._executions += 1

        if self._update_snapshots:
            serialized_data = self._serializer.encode(data)
            self._io_class.write(serialized_data, index=executions)
            return True

        deserialized = self._recall_data(index=executions)
        if deserialized is None:
            return self._fail(
                f"{error_style('SnapshotError:')} Snapshot does not exist."
            )

        if not self._is_equal(data, deserialized):
            return self._fail(
                [
                    error_style("SnapshotError: Snapshot does not match."),
                    error_style(f"  - {data}"),
                    error_style(f"  + {deserialized}"),
                ]
            )
        return True

    def _recall_data(self, index):
        try:
            saved_data = self._io_class.read(index=index)
            return self._serializer.decode(saved_data)
        except SnapshotDoesNotExist:
            return None

    def _is_equal(self, a, b):
        return a == b

    def assert_match(self, data):
        return self._assert(data)
