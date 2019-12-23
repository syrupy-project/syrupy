"""
Syrupy snapshot assertion module
"""

from collections import namedtuple
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Type,
)

from .exceptions import SnapshotDoesNotExist
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
    """
    Syrupy snapshot fixture
    """

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
        self._serializer: Optional["AbstractSnapshotSerializer"] = None
        self._test_location = test_location
        self._executions = 0
        self._execution_results: Dict[int, "AssertionResult"] = {}

        self._session: "SnapshotSession" = session
        self._session.register_request(self)

    @property
    def serializer(self) -> "AbstractSnapshotSerializer":
        """
        Assertion serializer
        """
        if self._serializer is None:
            self._serializer = self._serializer_class(test_location=self._test_location)
        return self._serializer

    @property
    def num_executions(self) -> int:
        """
        Number of times the assertion fixture has been executed
        """
        return int(self._executions)

    @property
    def executions(self) -> Dict[int, AssertionResult]:
        """
        Results of fixture assertions by execution index
        """
        return self._execution_results

    @property
    def discovered_snapshots(self) -> "SnapshotFiles":
        """
        Find and return all discovered snapshot files
        """
        return {
            filepath: self.serializer.discover_snapshots(filepath)
            for filepath in walk_snapshot_dir(self.serializer.dirname)
        }

    def with_class(
        self, serializer_class: Optional[Type["AbstractSnapshotSerializer"]] = None,
    ) -> "SnapshotAssertion":
        """
        Create new assertion with a custom serializer class.
        Useful for extending the initial fixture to be used on more complex objects.
        """
        return self.__class__(
            update_snapshots=self._update_snapshots,
            test_location=self._test_location,
            serializer_class=serializer_class or self._serializer_class,
            session=self._session,
        )

    def assert_match(self, data: "SerializableData") -> None:
        """
        Asserts if assertion matches data
        """
        assert self == data

    def get_assert_diff(self, data: "SerializableData") -> List[str]:
        """
        Get the different between data given and the existing snapshot
        """
        assertion_result = self._execution_results[self.num_executions - 1]
        snapshot_data = assertion_result.recalled
        if snapshot_data is None:
            return ["Snapshot does not exist!"]

        if not assertion_result.success:
            return [f"- {data}", f"+ {snapshot_data}"]

        return []

    def __repr__(self) -> str:
        return f"<SnapshotAssertion ({self.num_executions})>"

    def __call__(self, data: "SerializableData") -> bool:
        return self._assert(data)

    def __eq__(self, other: "SerializableData") -> bool:
        return self._assert(other)

    def _assert(self, data: "SerializableData") -> bool:
        snapshot_file = self.serializer.get_filepath(self.num_executions)
        snapshot_name = self.serializer.get_snapshot_name(self.num_executions)
        try:
            snapshot_data = self._recall_data(index=self.num_executions)
            matches = snapshot_data is not None and data == snapshot_data
            assertion_success = matches
            if not matches and self._update_snapshots:
                self.serializer.create_or_update_snapshot(
                    serialized_data=data, index=self.num_executions
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
                asserted=data,
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
