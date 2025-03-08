# noqa: A005
from typing import (
    Any,
    Callable,
    Hashable,
    Optional,
    Tuple,
    Type,
    Union,
)

SnapshotIndex = Union[int, str]
SerializableData = Any
SerializedData = Union[str, bytes]
PropertyName = Hashable
PropertyValueType = Type[SerializableData]
PropertyPathEntry = Tuple[PropertyName, PropertyValueType]
PropertyPath = Tuple[PropertyPathEntry, ...]
try:
    from mypy_extensions import NamedArg

    PropertyMatcher = Callable[
        [
            NamedArg(SerializableData, "data"),  # noqa: F821
            NamedArg(PropertyPath, "path"),  # noqa: F821
        ],
        Optional[SerializableData],
    ]
    PropertyFilter = Callable[
        [
            NamedArg(PropertyName, "prop"),  # noqa: F821
            NamedArg(PropertyPath, "path"),  # noqa: F821
        ],
        bool,
    ]

except ImportError:
    globals()["PropertyMatcher"] = Callable[..., Optional[SerializableData]]
    globals()["PropertyFilter"] = Callable[..., bool]
