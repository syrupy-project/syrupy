from collections.abc import Callable, Hashable
from typing import (
    Any,
)

SnapshotIndex = int | str
SerializableData = Any
SerializedData = str | bytes
PropertyName = Hashable
PropertyValueType = type[SerializableData]
PropertyPathEntry = tuple[PropertyName, PropertyValueType]
PropertyPath = tuple[PropertyPathEntry, ...]
try:
    from mypy_extensions import NamedArg

    PropertyMatcher = Callable[
        [
            NamedArg(SerializableData, "data"),
            NamedArg(PropertyPath, "path"),
        ],
        SerializableData | None,
    ]
    PropertyFilter = Callable[
        [
            NamedArg(PropertyName, "prop"),
            NamedArg(PropertyPath, "path"),
        ],
        bool,
    ]

except ImportError:
    globals()["PropertyMatcher"] = Callable[..., SerializableData | None]
    globals()["PropertyFilter"] = Callable[..., bool]
