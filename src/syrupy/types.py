from typing import (
    Any,
    Hashable,
    Optional,
    Tuple,
    Type,
    Union,
)

SerializableData = Any
SerializedData = Union[str, bytes]
PropertyName = Hashable
PropertyValueType = Type[SerializableData]
PropertyPathEntry = Tuple[PropertyName, PropertyValueType]
PropertyPath = Tuple[PropertyPathEntry, ...]
try:
    # Python minimum version 3.8
    # https://docs.python.org/3/library/typing.html#typing.Protocol
    from typing import Protocol

    class PropertyMatcher(Protocol):
        def __call__(
            self,
            *,
            data: "SerializableData",
            path: "PropertyPath",
        ) -> Optional["SerializableData"]:
            ...

    class PropertyFilter(Protocol):
        def __call__(self, *, prop: "PropertyName", path: "PropertyPath") -> bool:
            ...


except ImportError:
    pass
