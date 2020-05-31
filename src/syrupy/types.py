from typing import (
    Any,
    Callable,
    Optional,
    Tuple,
    Union,
)


SerializableData = Any
SerializedData = Union[str, bytes]
PropertyMatcher = Callable[[str, Any, Tuple[str]], Optional[Any]]
