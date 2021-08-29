import traceback
from gettext import gettext
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    Union,
)

import attr

from .exceptions import SnapshotDoesNotExist

if TYPE_CHECKING:
    from .extensions.base import AbstractSyrupyExtension
    from .location import PyTestLocation
    from .session import SnapshotSession
    from .types import (
        PropertyFilter,
        PropertyMatcher,
        SerializableData,
        SerializedData,
    )


@attr.s
class AssertionResult:
    snapshot_location: str = attr.ib()
    snapshot_name: str = attr.ib()
    asserted_data: Optional["SerializedData"] = attr.ib()
    recalled_data: Optional["SerializedData"] = attr.ib()
    created: bool = attr.ib()
    updated: bool = attr.ib()
    success: bool = attr.ib()
    exception: Optional[Exception] = attr.ib()

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
    _test_location: "PyTestLocation" = attr.ib(kw_only=True)
    _update_snapshots: bool = attr.ib(kw_only=True)
    _exclude: Optional["PropertyFilter"] = attr.ib(
        init=False, default=None, kw_only=True
    )
    _custom_index: Optional[str] = attr.ib(init=False, default=None, kw_only=True)
    _extension: Optional["AbstractSyrupyExtension"] = attr.ib(
        init=False, default=None, kw_only=True
    )
    _executions: int = attr.ib(init=False, default=0, kw_only=True)
    _execution_results: Dict[int, "AssertionResult"] = attr.ib(
        init=False, factory=dict, kw_only=True
    )
    _matcher: Optional["PropertyMatcher"] = attr.ib(
        init=False, default=None, kw_only=True
    )
    _post_assert_actions: List[Callable[..., None]] = attr.ib(
        init=False, factory=list, kw_only=True
    )

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

    @property
    def index(self) -> Union[str, int]:
        if self._custom_index:
            return self._custom_index
        return self.num_executions

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

    def _serialize(self, data: "SerializableData") -> "SerializedData":
        return self.extension.serialize(
            data, exclude=self._exclude, matcher=self._matcher
        )

    def get_assert_diff(self) -> List[str]:
        assertion_result = self._execution_results[self.num_executions - 1]
        if assertion_result.exception:
            lines = [
                line
                for lines in traceback.format_exception(
                    assertion_result.exception.__class__,
                    assertion_result.exception,
                    assertion_result.exception.__traceback__,
                )
                for line in lines.splitlines()
            ]
            # Rotate to place exception with message at first line
            return lines[-1:] + lines[:-1]
        snapshot_data = assertion_result.recalled_data
        serialized_data = assertion_result.asserted_data or ""
        diff: List[str] = []
        if snapshot_data is None:
            diff.append(
                gettext("Snapshot '{}' does not exist!").format(
                    assertion_result.snapshot_name
                )
            )
        if not assertion_result.success:
            diff.extend(self.extension.diff_lines(serialized_data, snapshot_data or ""))
        return diff

    def __with_prop(self, prop_name: str, prop_value: Any) -> None:
        setattr(self, prop_name, prop_value)
        self._post_assert_actions.append(lambda: setattr(self, prop_name, None))

    def __call__(
        self,
        *,
        exclude: Optional["PropertyFilter"] = None,
        extension_class: Optional[Type["AbstractSyrupyExtension"]] = None,
        matcher: Optional["PropertyMatcher"] = None,
        name: Optional[str] = None,
    ) -> "SnapshotAssertion":
        """
        Modifies assertion instance options
        """
        if exclude:
            self.__with_prop("_exclude", exclude)
        if extension_class:
            self.__with_prop("_extension", self.__init_extension(extension_class))
        if matcher:
            self.__with_prop("_matcher", matcher)
        if name:
            self.__with_prop("_custom_index", name)
        return self

    def __dir__(self) -> List[str]:
        return ["name", "num_executions"]

    def __eq__(self, other: "SerializableData") -> bool:
        return self._assert(other)

    def _assert(self, data: "SerializableData") -> bool:
        snapshot_location = self.extension.get_location(index=self.index)
        snapshot_name = self.extension.get_snapshot_name(index=self.index)
        snapshot_data: Optional["SerializedData"] = None
        serialized_data: Optional["SerializedData"] = None
        matches = False
        assertion_success = False
        assertion_exception = None
        try:
            snapshot_data = self._recall_data()
            serialized_data = self._serialize(data)
            matches = snapshot_data is not None and self.extension.matches(
                serialized_data=serialized_data, snapshot_data=snapshot_data
            )
            assertion_success = matches
            if not matches and self._update_snapshots:
                self.extension.write_snapshot(
                    data=serialized_data,
                    index=self.index,
                )
                assertion_success = True
            return assertion_success
        except Exception as e:
            assertion_exception = e
            return False
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
                exception=assertion_exception,
            )
            self._executions += 1
            self._post_assert()

    def _post_assert(self) -> None:
        """
        Restores assertion instance options
        """
        while self._post_assert_actions:
            self._post_assert_actions.pop()()

    def _recall_data(self) -> Optional["SerializableData"]:
        try:
            return self.extension.read_snapshot(index=self.index)
        except SnapshotDoesNotExist:
            return None
