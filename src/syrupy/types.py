from typing import (
    Any,
    Callable,
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
PropertyMatcher = Callable[..., Optional[SerializableData]]
PropertyFilter = Callable[..., bool]
