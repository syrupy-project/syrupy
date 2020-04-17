from gettext import gettext
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    List,
    Optional,
    Type,
)

import attr

from .exceptions import SnapshotDoesNotExist


if TYPE_CHECKING:
    from .location import TestLocation
    from .extensions.base import AbstractSyrupyExtension
    from .session import SnapshotSession
    from .types import SerializableData, SerializedData  # noqa: F401


@attr.s
class AssertionResult:
    snapshot_location: str = attr.ib()
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
    _extension_class: Type["AbstractSyrupyExtension"] = attr.ib(kw_only=True)
    _test_location: "TestLocation" = attr.ib(kw_only=True)
    _update_snapshots: bool = attr.ib(kw_only=True)
    _extension: Optional["AbstractSyrupyExtension"] = attr.ib(init=False, default=None)
    _executions: int = attr.ib(init=False, default=0)
    _execution_results: Dict[int, "AssertionResult"] = attr.ib(init=False, factory=dict)
    _post_assert_actions: List[Callable[..., None]] = attr.ib(init=False, factory=list)

    def __attrs_post_init__(self) -> None:
        self._session.register_request(self)

    def __init_extension(
        self, extension_class: Type["AbstractSyrupyExtension"]
    ) -> "AbstractSyrupyExtension":
        return extension_class(test_location=self._test_location)

    @property
    def extension(self) -> "AbstractSyrupyExtension":
        if not self._extension:
            self._extension = self.__init_extension(self._extension_class)
        return self._extension

    @property
    def num_executions(self) -> int:
        return int(self._executions)

    @property
    def executions(self) -> Dict[int, AssertionResult]:
        return self._execution_results

    def use_extension(
        self, extension_class: Optional[Type["AbstractSyrupyExtension"]] = None
    ) -> "SnapshotAssertion":
        """
        Creates a new snapshot assertion fixture with the same options but using
        specified extension class. This does not preserve assertion index or state.
        """
        return self.__class__(
            update_snapshots=self._update_snapshots,
            test_location=self._test_location,
            extension_class=extension_class or self._extension_class,
            session=self._session,
        )

    def assert_match(self, data: "SerializableData") -> None:
        assert self == data

    def get_assert_diff(self, data: "SerializableData") -> List[str]:
        assertion_result = self._execution_results[self.num_executions - 1]
        snapshot_data = assertion_result.recalled_data
        serialized_data = self.extension.serialize(data)
        diff: List[str] = []
        if snapshot_data is None:
            diff.append(gettext("Snapshot does not exist!"))
        if not assertion_result.success:
            diff.extend(self.extension.diff_lines(serialized_data, snapshot_data or ""))
        return diff

    def __call__(
        self, *, extension_class: Optional[Type["AbstractSyrupyExtension"]]
    ) -> "SnapshotAssertion":
        """
        Modifies assertion instance options
        """
        if extension_class:
            self._extension = self.__init_extension(extension_class)

            def clear_extension() -> None:
                self._extension = None

            self._post_assert_actions.append(clear_extension)
        return self

    def __repr__(self) -> str:
        attrs_to_repr = ["name", "num_executions"]
        attrs_repr = ", ".join(f"{a}={repr(getattr(self, a))}" for a in attrs_to_repr)
        return f"SnapshotAssertion({attrs_repr})"

    def __eq__(self, other: "SerializableData") -> bool:
        return self._assert(other)

    def _assert(self, data: "SerializableData") -> bool:
        snapshot_location = self.extension.get_location(index=self.num_executions)
        snapshot_name = self.extension.get_snapshot_name(index=self.num_executions)
        snapshot_data: Optional["SerializedData"] = None
        serialized_data: Optional["SerializedData"] = None
        matches = False
        assertion_success = False
        try:
            snapshot_data = self._recall_data(index=self.num_executions)
            serialized_data = self.extension.serialize(data)
            matches = snapshot_data is not None and serialized_data == snapshot_data
            assertion_success = matches
            if not matches and self._update_snapshots:
                self.extension.write_snapshot(
                    data=serialized_data, index=self.num_executions
                )
                assertion_success = True
            return assertion_success
        finally:
            snapshot_created = snapshot_data is None and assertion_success
            snapshot_updated = matches is False and assertion_success
            self._execution_results[self._executions] = AssertionResult(
                snapshot_location=snapshot_location,
                snapshot_name=snapshot_name,
                recalled_data=snapshot_data,
                asserted_data=serialized_data,
                success=assertion_success,
                created=snapshot_created,
                updated=snapshot_updated,
            )
            self._executions += 1
            self._post_assert()

    def _post_assert(self) -> None:
        """
        Restores assertion instance options
        """
        while self._post_assert_actions:
            self._post_assert_actions.pop()()

    def _recall_data(self, index: int) -> Optional["SerializableData"]:
        try:
            return self.extension.read_snapshot(index=index)
        except SnapshotDoesNotExist:
            return None
