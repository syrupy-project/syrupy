from collections import namedtuple
from itertools import zip_longest
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Type,
)

from .exceptions import SnapshotDoesNotExist
from .terminal import (
    error_style,
    green,
    red,
    success_style,
)
from .utils import walk_snapshot_dir


if TYPE_CHECKING:
    from .location import TestLocation
    from .serializers.base import AbstractSnapshotSerializer
    from .session import SnapshotSession
    from .types import SerializableData, SnapshotFiles


AssertionResult = namedtuple(
    "AssertionResult",
    ["asserted", "created", "file", "name", "recalled", "success", "updated"],
)


class SnapshotAssertion:
    def __init__(
        self,
        *,
        update_snapshots: bool,
        serializer_class: Type["AbstractSnapshotSerializer"],
        test_location: "TestLocation",
        session: "SnapshotSession",
    ):
        self._update_snapshots = update_snapshots
        self._serializer_class = serializer_class
        self._test_location = test_location
        self._executions = 0
        self._execution_results: Dict[int, "AssertionResult"] = {}

        self._session: "SnapshotSession" = session
        self._session.register_request(self)

    @property
    def serializer(self) -> "AbstractSnapshotSerializer":
        if not getattr(self, "_serializer", None):
            self._serializer: "AbstractSnapshotSerializer" = self._serializer_class(
                test_location=self._test_location
            )
        return self._serializer

    @property
    def num_executions(self) -> int:
        return int(self._executions)

    @property
    def executions(self) -> Dict[int, AssertionResult]:
        return self._execution_results

    @property
    def discovered_snapshots(self) -> "SnapshotFiles":
        empty = {"empty snapshot file"}
        return {
            filepath: self.serializer.discover_snapshots(filepath) or empty
            for filepath in walk_snapshot_dir(self.serializer.dirname)
            if filepath.endswith(self.serializer.file_extension)
        }

    def with_class(
        self, serializer_class: Optional[Type["AbstractSnapshotSerializer"]] = None,
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
        assertion_result = self._execution_results[self.num_executions - 1]
        snapshot_data = assertion_result.recalled
        serialized_data = self.serializer.serialize(data)
        if snapshot_data is None:
            return ["Snapshot does not exist!"]

        diff = []
        if not assertion_result.success:
            received = serialized_data.splitlines()
            stored = snapshot_data.splitlines()

            marker_stored = success_style("-")
            marker_received = error_style("+")

            for received_line, stored_line in zip_longest(received, stored):
                if received_line is None:
                    diff.append(f"{marker_stored} {green(stored_line)}")
                elif stored_line is None:
                    diff.append(f"{marker_received} {red(received_line)}")
                elif received_line != stored_line:
                    diff.extend(
                        [
                            f"{marker_stored} {green(stored_line)}",
                            f"{marker_received} {red(received_line)}",
                        ]
                    )

        return diff

    def __repr__(self) -> str:
        return f"<SnapshotAssertion ({self.num_executions})>"

    def __call__(self, data: "SerializableData") -> bool:
        return self._assert(data)

    def __eq__(self, other: "SerializableData") -> bool:
        return self._assert(other)

    def _assert(self, data: "SerializableData") -> bool:
        matches = False
        assertion_success = False
        snapshot_data = None
        serialized_data = None
        try:
            snapshot_file = self.serializer.get_filepath(self.num_executions)
            snapshot_name = self.serializer.get_snapshot_name(self.num_executions)
            snapshot_data = self._recall_data(index=self.num_executions)
            serialized_data = self.serializer.serialize(data)
            matches = snapshot_data is not None and serialized_data == snapshot_data
            assertion_success = matches
            if not matches and self._update_snapshots:
                self.serializer.create_or_update_snapshot(
                    data=data, index=self.num_executions
                )
                assertion_success = True
            return assertion_success
        finally:
            snapshot_created = snapshot_data is None and assertion_success
            snapshot_updated = matches is False and assertion_success
            self._execution_results[self._executions] = AssertionResult(
                file=snapshot_file,
                name=snapshot_name,
                recalled=snapshot_data,
                asserted=serialized_data,
                success=assertion_success,
                created=snapshot_created,
                updated=snapshot_updated,
            )
            self._executions += 1

    def _recall_data(self, index: int) -> Optional["SerializableData"]:
        try:
            return self.serializer.read_snapshot(index=index)
        except SnapshotDoesNotExist:
            return None
