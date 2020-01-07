from gettext import gettext
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Type,
)

import attr

from .data import (
    SnapshotEmptyFile,
    SnapshotFile,
    SnapshotFiles,
)
from .exceptions import SnapshotDoesNotExist
from .utils import walk_snapshot_dir


if TYPE_CHECKING:
    from .location import TestLocation
    from .serializers.base import AbstractSnapshotSerializer
    from .session import SnapshotSession
    from .types import SerializableData, SerializedData  # noqa: F401


@attr.s
class AssertionResult(object):
    snapshot_filepath: str = attr.ib()
    snapshot_name: str = attr.ib()
    asserted_data: Optional["SerializedData"] = attr.ib()
    recalled_data: Optional["SerializedData"] = attr.ib()
    created: bool = attr.ib()
    updated: bool = attr.ib()
    success: bool = attr.ib()

    @property
    def final_data(self) -> Optional["SerializedData"]:
        if self.created or self.updated:
            return self.asserted_data
        return self.recalled_data


@attr.s(cmp=False, repr=False)
class SnapshotAssertion:
    name: str = attr.ib(default="snapshot")
    _session: "SnapshotSession" = attr.ib(kw_only=True)
    _serializer_class: Type["AbstractSnapshotSerializer"] = attr.ib(kw_only=True)
    _test_location: "TestLocation" = attr.ib(kw_only=True)
    _update_snapshots: bool = attr.ib(kw_only=True)
    _executions: int = attr.ib(init=False, default=0, kw_only=True)
    _execution_results: Dict[int, "AssertionResult"] = attr.ib(
        init=False, factory=dict, kw_only=True
    )

    def __attrs_post_init__(self) -> None:
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
        discovered_files: "SnapshotFiles" = SnapshotFiles()
        for filepath in walk_snapshot_dir(self.serializer.dirname):
            if filepath.endswith(self.serializer.file_extension):
                snapshot_file = self.serializer.discover_snapshots(filepath)
                if not snapshot_file.has_snapshots:
                    snapshot_file = SnapshotEmptyFile(filepath=filepath)
            else:
                snapshot_file = SnapshotFile(filepath=filepath)
            discovered_files.add(snapshot_file)
        return discovered_files

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
        snapshot_data = assertion_result.recalled_data
        serialized_data = self.serializer.serialize(data)
        if snapshot_data is None:
            return [gettext("Snapshot does not exist!")]

        diff: List[str] = []
        if not assertion_result.success:
            diff.extend(self.serializer.diff_lines(serialized_data, snapshot_data))
        return diff

    def __repr__(self) -> str:
        attrs_to_repr = ["name", "num_executions"]
        attrs_repr = ", ".join(f"{a}={repr(getattr(self, a))}" for a in attrs_to_repr)
        return f"SnapshotAssertion({attrs_repr})"

    def __eq__(self, other: "SerializableData") -> bool:
        return self._assert(other)

    def _assert(self, data: "SerializableData") -> bool:
        matches = False
        assertion_success = False
        snapshot_data: Optional["SerializedData"] = None
        serialized_data: Optional["SerializedData"] = None
        try:
            snapshot_filepath = self.serializer.get_filepath(self.num_executions)
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
                snapshot_filepath=snapshot_filepath,
                snapshot_name=snapshot_name,
                recalled_data=snapshot_data,
                asserted_data=serialized_data,
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
