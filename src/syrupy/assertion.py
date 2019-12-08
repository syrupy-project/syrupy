from typing import Any, Callable, List, Optional, Type, TypeVar, TYPE_CHECKING

from .types import SerializableData
from .exceptions import SnapshotDoesNotExist

if TYPE_CHECKING:
    from .serializer import SnapshotSerializer
    from .location import TestLocation
    from .session import SnapshotSession


class SnapshotAssertion:
    def __init__(
        self,
        *,
        update_snapshots: bool,
        serializer_class: Type["SnapshotSerializer"],
        test_location: "TestLocation",
        session: "SnapshotSession",
    ):
        self._update_snapshots = update_snapshots
        self._serializer_class = serializer_class
        self._test_location = test_location
        self._executions = 0

        self._session: "SnapshotSession" = session
        self._session.register_request(self)

    @property
    def serializer(self) -> "SnapshotSerializer":
        if not getattr(self, "_serializer", None):
            self._serializer: "SnapshotSerializer" = self._serializer_class(
                test_location=self._test_location, file_hook=self._file_hook
            )
        return self._serializer

    @property
    def num_executions(self) -> int:
        return int(self._executions)

    def with_class(
        self, serializer_class: Optional[Type["SnapshotSerializer"]] = None,
    ) -> "SnapshotAssertion":
        return self.__class__(
            update_snapshots=self._update_snapshots,
            test_location=self._test_location,
            serializer_class=serializer_class or self._serializer_class,
            session=self._session,
        )

    def assert_match(self, data: "SerializableData") -> None:
        assert self == data

    def get_assert_diff(self, data: "SerializableData") -> List[str]:
        snapshot_data = self._recall_data(index=self.num_executions - 1)
        if snapshot_data is None:
            return ["Snapshot does not exist!"]

        if data != snapshot_data:
            return [f"- {data}", f"+ {snapshot_data}"]

        return []

    def _file_hook(self, filepath: str, snapshot_name: str) -> None:
        self._session.add_visited_snapshots({filepath: {snapshot_name}})

    def __repr__(self) -> str:
        return f"<SnapshotAssertion ({self.num_executions})>"

    def __call__(self, data: "SerializableData") -> bool:
        return self._assert(data)

    def __eq__(self, other: "SerializableData") -> bool:
        return self._assert(other)

    def _assert(self, data: "SerializableData") -> bool:
        self._session.register_assertion(self)
        try:
            snapshot_data = self._recall_data(index=self.num_executions)
            matches = snapshot_data is not None and data == snapshot_data
            if not matches and self._update_snapshots:
                self.serializer.create_or_update_snapshot(
                    serialized_data=data, index=self.num_executions
                )
                return True
            return matches
        finally:
            self._executions += 1

    def _recall_data(self, index: int) -> Optional["SerializableData"]:
        try:
            return self.serializer.read_snapshot(index=index)
        except SnapshotDoesNotExist:
            return None
