# noqa: A005
from collections.abc import Hashable
from typing import (
    Any,
    Callable,
    Optional,
    Union,
)

SnapshotIndex = Union[int, str]
SerializableData = Any
SerializedData = Union[str, bytes]
PropertyName = Hashable
PropertyValueType = type[SerializableData]
PropertyPathEntry = tuple[PropertyName, PropertyValueType]
PropertyPath = tuple[PropertyPathEntry, ...]
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
