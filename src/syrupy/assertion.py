import traceback
import pytest
import os
from typing import Any, Callable, List, Optional, Type

from .exceptions import SnapshotDoesNotExist

from .io import SnapshotIO
from .serializer import SnapshotSerializer
from .location import TestLocation


class SnapshotAssertion:
    def __init__(
        self,
        *,
        update_snapshots: bool,
        io_class: Type[SnapshotIO],
        serializer_class: Type[SnapshotSerializer],
        test_location: TestLocation,
        session,
    ):
        self._update_snapshots = update_snapshots
        self._io_class = io_class
        self._serializer_class = serializer_class
        self._test_location = test_location
        self._executions = 0

        from .session import SnapshotSession

        self._session: SnapshotSession = session
        self._session.register_request(self)

    @property
    def io(self) -> SnapshotIO:
        if not getattr(self, "_io", None):
            self._io = self._io_class(
                test_location=self._test_location, file_hook=self._file_hook
            )
        return self._io

    @property
    def serializer(self) -> SnapshotSerializer:
        if not getattr(self, "_serializer", None):
            self._serializer = self._serializer_class()
        return self._serializer

    @property
    def num_executions(self) -> int:
        return int(self._executions)

    def with_class(
        self,
        io_class: Type[SnapshotIO] = None,
        serializer_class: Type[SnapshotSerializer] = None,
    ):
        return self.__class__(
            update_snapshots=self._update_snapshots,
            test_location=self._test_location,
            io_class=io_class or self._io_class,
            serializer_class=serializer_class or self._serializer_class,
            session=self._session,
        )

    def assert_match(self, data):
        assert self == data

    def get_assert_diff(self, data) -> List[str]:
        deserialized = self._recall_data(index=self.num_executions - 1)
        if deserialized is None:
            return ["Snapshot does not exist!"]

        if data != deserialized:
            return [f"- {data}", f"+ {deserialized}"]

        return []

    def _file_hook(self, filepath, snapshot_name):
        self._session.add_visited_snapshots({filepath: {snapshot_name}})

    def __repr__(self) -> str:
        return f"<SnapshotAssertion ({self.num_executions})>"

    def __call__(self, data) -> bool:
        return self._assert(data)

    def __eq__(self, other) -> bool:
        return self._assert(other)

    def _assert(self, data) -> bool:
        self._session.register_assertion(self)
        try:
            if self._update_snapshots:
                serialized_data = self.serializer.encode(data)
                self.io.create_or_update_snapshot(
                    serialized_data, index=self.num_executions
                )
                return True

            deserialized = self._recall_data(index=self.num_executions)
            if deserialized is None or data != deserialized:
                return False
            return True
        finally:
            self._executions += 1

    def _recall_data(self, index: int) -> Optional[Any]:
        try:
            saved_data = self.io.read_snapshot(index=index)
            return self.serializer.decode(saved_data)
        except SnapshotDoesNotExist:
            return None
