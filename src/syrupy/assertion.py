import traceback
from collections import namedtuple
from dataclasses import (
    dataclass,
    field,
)
from gettext import gettext
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
)

from .exceptions import SnapshotDoesNotExist
from .extensions.amber.serializer import Repr

if TYPE_CHECKING:
    from .extensions.base import AbstractSyrupyExtension
    from .location import PyTestLocation
    from .session import SnapshotSession
    from .types import (
        PropertyFilter,
        PropertyMatcher,
        SerializableData,
        SerializedData,
        SnapshotIndex,
    )


@dataclass
class AssertionResult:
    snapshot_location: str
    snapshot_name: str
    asserted_data: Optional["SerializedData"]
    recalled_data: Optional["SerializedData"]
    created: bool
    updated: bool
    success: bool
    exception: Optional[Exception]

    @property
    def final_data(self) -> Optional["SerializedData"]:
        if self.created or self.updated:
            return self.asserted_data
        return self.recalled_data


@dataclass(eq=False, order=False, repr=False)
class SnapshotAssertion:
    session: "SnapshotSession"
    extension_class: Type["AbstractSyrupyExtension"]
    test_location: "PyTestLocation"
    update_snapshots: bool

    _exclude: Optional["PropertyFilter"] = field(
        init=False,
        default=None,
    )
    _custom_index: Optional[str] = field(
        init=False,
        default=None,
    )
    _extension: Optional["AbstractSyrupyExtension"] = field(
        init=False,
        default=None,
    )
    _executions: int = field(
        init=False,
        default=0,
    )
    _execution_results: Dict[int, "AssertionResult"] = field(
        init=False,
        default_factory=dict,
    )
    _execution_name_index: Dict["SnapshotIndex", int] = field(
        init=False, default_factory=dict
    )
    _matcher: Optional["PropertyMatcher"] = field(
        init=False,
        default=None,
    )
    _post_assert_actions: List[Callable[..., None]] = field(
        init=False,
        default_factory=list,
    )

    def __post_init__(self) -> None:
        self.session.register_request(self)

    def __init_extension(
        self, extension_class: Type["AbstractSyrupyExtension"]
    ) -> "AbstractSyrupyExtension":
        return extension_class(test_location=self.test_location)

    @property
    def extension(self) -> "AbstractSyrupyExtension":
        if not self._extension:
            self._extension = self.__init_extension(self.extension_class)
        return self._extension

    @property
    def num_executions(self) -> int:
        return int(self._executions)

    @property
    def executions(self) -> Dict[int, "AssertionResult"]:
        return self._execution_results

    @property
    def index(self) -> "SnapshotIndex":
        if self._custom_index:
            return self._custom_index
        return self.num_executions

    @property
    def name(self) -> str:
        return self._custom_index or "snapshot"

    @property
    def __repr(self) -> "SerializableData":
        SnapshotAssertionRepr = namedtuple(  # type: ignore
            "SnapshotAssertion", ["name", "num_executions"]
        )
        assertion_result = self.executions.get(
            (self._custom_index and self._execution_name_index.get(self._custom_index))
            or self.num_executions - 1
        )
        return (
            Repr(str(assertion_result.final_data))
            if assertion_result
            else SnapshotAssertionRepr(
                name=self.name,
                num_executions=self.num_executions,
            )
        )

    @property
    def __matcher(self) -> "PropertyMatcher":
        """
        Get matcher that replaces `SnapshotAssertion` with one that can be serialized
        """

        def _matcher(**kwargs: Any) -> Optional["SerializableData"]:
            maybe_assertion = kwargs.get("data")
            if isinstance(maybe_assertion, SnapshotAssertion):
                return maybe_assertion.__repr
            if self._matcher:
                return self._matcher(**kwargs)
            return maybe_assertion

        return _matcher

    def use_extension(
        self, extension_class: Optional[Type["AbstractSyrupyExtension"]] = None
    ) -> "SnapshotAssertion":
        """
        Creates a new snapshot assertion fixture with the same options but using
        specified extension class. This does not preserve assertion index or state.
        """
        return self.__class__(
            update_snapshots=self.update_snapshots,
            test_location=self.test_location,
            extension_class=extension_class or self.extension_class,
            session=self.session,
        )

    def assert_match(self, data: "SerializableData") -> None:
        assert self == data

    def _serialize(self, data: "SerializableData") -> "SerializedData":
        return self.extension.serialize(
            data, exclude=self._exclude, matcher=self.__matcher
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
        diff: Optional["SnapshotIndex"] = None,
        exclude: Optional["PropertyFilter"] = None,
        extension_class: Optional[Type["AbstractSyrupyExtension"]] = None,
        matcher: Optional["PropertyMatcher"] = None,
        name: Optional["SnapshotIndex"] = None,
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
        if diff is not None:
            self.__with_prop("_snapshot_diff", diff)
        return self

    def __repr__(self) -> str:
        return str(self._serialize(self.__repr))

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
            snapshot_data = self._recall_data(index=self.index)
            serialized_data = self._serialize(data)
            snapshot_diff = getattr(self, "_snapshot_diff", None)
            if snapshot_diff is not None:
                snapshot_data_diff = self._recall_data(index=snapshot_diff)
                if snapshot_data_diff is None:
                    raise SnapshotDoesNotExist()
                serialized_data = self.extension.diff_snapshots(
                    serialized_data=serialized_data,
                    snapshot_data=snapshot_data_diff,
                )
            matches = snapshot_data is not None and self.extension.matches(
                serialized_data=serialized_data, snapshot_data=snapshot_data
            )
            assertion_success = matches
            if not matches and self.update_snapshots:
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
            self._execution_name_index[self.index] = self._executions
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

    def _recall_data(self, index: "SnapshotIndex") -> Optional["SerializableData"]:
        try:
            return self.extension.read_snapshot(index=index)
        except SnapshotDoesNotExist:
            return None
