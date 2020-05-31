from typing import (
    Any,
    Callable,
    Hashable,
    Optional,
    Tuple,
    Union,
)


SerializableData = Any
SerializedData = Union[str, bytes]
PropertyPath = Tuple[Hashable, ...]
PropertyMatcher = Callable[[SerializableData, PropertyPath], Optional[SerializableData]]
