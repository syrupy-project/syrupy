import traceback
import pytest
import os
from typing import List, Optional, Any

from .exceptions import SnapshotDoesNotExist
from .terminal import error_style, bold

from .io import SnapshotIO
from .serializer import SnapshotSerializer
from .location import TestLocation


class SnapshotAssertion:
    def __init__(
        self,
        *,
        update_snapshots: bool,
        io_class: SnapshotIO,
        serializer_class: SnapshotSerializer,
        test_location: TestLocation,
    ):
        self._update_snapshots = update_snapshots
        self._io_class = io_class
        self._serializer_class = serializer_class
        self._test_location = test_location
        self._executions = 0

    @property
    def io(self):
        if not getattr(self, "_io", None):
            self._io = self._io_class(test_location=self._test_location)
        return self._io

    @property
    def serializer(self):
        if not getattr(self, "_serializer", None):
            self._serializer = self._serializer_class()
        return self._serializer

    def with_class(
        self, io_class: SnapshotIO = None, serializer_class: SnapshotSerializer = None
    ):
        return self.__class__(
            update_snapshots=self._update_snapshots,
            test_location=self._test_location,
            io_class=io_class or self._io_class,
            serializer_class=serializer_class or self._serializer_class,
        )

    def assert_match(self, data) -> bool:
        return self._assert(data)

    def get_assert_diff(self, data) -> List[str]:
        deserialized = self._recall_data(index=self._executions - 1)
        if deserialized is None:
            return ["Snapshot does not exist!"]

        if data != deserialized:
            return [f"- {data}", f"+ {deserialized}"]

        return ["Assert diff!"]

    def __repr__(self) -> str:
        return f"<SnapshotAssertion ({self._executions})>"

    def __call__(self, data) -> bool:
        return self._assert(data)

    def __eq__(self, other) -> bool:
        return self._assert(other)

    def _assert(self, data) -> bool:
        executions = self._executions
        self._executions += 1

        if self._update_snapshots:
            serialized_data = self.serializer.encode(data)
            self.io.write(serialized_data, index=executions)
            return True

        deserialized = self._recall_data(index=executions)
        if deserialized is None or data != deserialized:
            return False
        return True

    def _recall_data(self, index: int) -> Optional[Any]:
        try:
            saved_data = self.io.read(index=index)
            return self.serializer.decode(saved_data)
        except SnapshotDoesNotExist:
            return None
