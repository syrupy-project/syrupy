import functools
import os
from dataclasses import dataclass
from numbers import Number
from types import (
    GeneratorType,
    MappingProxyType,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Hashable,
    Iterable,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

from syrupy.constants import (
    SYMBOL_ELLIPSIS,
    TEXT_ENCODING,
)
from syrupy.data import (
    Snapshot,
    SnapshotFossil,
)

if TYPE_CHECKING:
    from syrupy.types import (
        PropertyFilter,
        PropertyMatcher,
        PropertyName,
        PropertyPath,
        SerializableData,
        SupportsRichComparison,
    )

    PropertyValueFilter = Callable[["PropertyName"], bool]
    PropertyValueGetter = Callable[
        ["SerializableData", "PropertyName"], "SerializableData"
    ]
    IterableEntries = Tuple[
        Iterable["PropertyName"],
        "PropertyValueGetter",
        Optional["PropertyValueFilter"],
    ]


@dataclass
class PreppedData(object):
    value_type: Type[object]
    # When value is a string it is ready to print as is
    value: Union[Optional[str], Iterable["PreppedData"]]
    key: Optional[Hashable] = None

    def with_key(self, key: Optional[Hashable]) -> "PreppedData":
        self.key = key
        return self


PreppedValue = Union[Optional[str], "PreppedData"]


class Repr:
    def __init__(self, _repr: str):
        self._repr = _repr

    def __repr__(self) -> str:
        return self._repr


def attr_getter(o: "SerializableData", p: "PropertyName") -> "SerializableData":
    return getattr(o, str(p))


def item_getter(o: "SerializableData", p: "PropertyName") -> "SerializableData":
    return o[p]


class DataSerializer:
    _indent: str = "  "
    _max_depth: int = 99
    _marker_comment: str = "# "
    _marker_divider: str = f"{_marker_comment}---"
    _marker_name: str = f"{_marker_comment}name:"
    _marker_crn: str = "\r\n"

    @classmethod
    def write_file(cls, snapshot_fossil: "SnapshotFossil") -> None:
        """
        Writes the snapshot data into the snapshot file that be read later.
        """
        filepath = snapshot_fossil.location
        with open(filepath, "w", encoding=TEXT_ENCODING, newline=None) as f:
            for snapshot in sorted(snapshot_fossil, key=lambda s: s.name):
                snapshot_data = str(snapshot.data)
                if snapshot_data is not None:
                    f.write(f"{cls._marker_name} {snapshot.name}\n")
                    for data_line in snapshot_data.splitlines(keepends=True):
                        f.write(cls.with_indent(data_line, 1))
                    f.write(f"\n{cls._marker_divider}\n")

    @classmethod
    @functools.lru_cache()
    def read_file(cls, filepath: str) -> "SnapshotFossil":
        """
        Read the raw snapshot data (str) from the snapshot file into a dict
        of snapshot name to raw data. This does not attempt any deserialization
        of the snapshot data.
        """
        name_marker_len = len(cls._marker_name)
        indent_len = len(cls._indent)
        snapshot_fossil = SnapshotFossil(location=filepath)
        try:
            with open(filepath, "r", encoding=TEXT_ENCODING, newline=None) as f:
                test_name = None
                snapshot_data = ""
                for line in f:
                    if line.startswith(cls._marker_name):
                        test_name = line[name_marker_len:].strip(f" {cls._marker_crn}")
                        snapshot_data = ""
                        continue
                    elif test_name is not None:
                        if line.startswith(cls._indent):
                            snapshot_data += line[indent_len:]
                        elif line.startswith(cls._marker_divider) and snapshot_data:
                            snapshot_fossil.add(
                                Snapshot(
                                    name=test_name,
                                    data=snapshot_data.rstrip(os.linesep),
                                )
                            )
        except FileNotFoundError:
            pass

        return snapshot_fossil

    @classmethod
    def serialize(
        cls,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> str:
        """
        After serializing, new line control characters are normalised. This is needed
        for interoperablity of snapshot matching between systems that do not use the
        same new line control characters. Example snapshots generated on windows os
        should not break when running the tests on a unix based system and vice versa.
        """
        prepped = cls._prepare(data, exclude=exclude, matcher=matcher)
        serialized = cls._serialize(prepped)
        return serialized.replace(cls._marker_crn, "\n").replace("\r", "\n")

    @classmethod
    def _prepare(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        exclude: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: Optional[Set[Any]] = None,
    ) -> "PreppedData":
        visited = set() if visited is None else visited
        data_id = id(data)
        if depth > cls._max_depth or data_id in visited:
            data = Repr(SYMBOL_ELLIPSIS)
        elif matcher:
            data = matcher(data=data, path=path)
        prep_kwargs = {
            "data": data,
            "depth": depth,
            "exclude": exclude,
            "matcher": matcher,
            "path": path,
            "visited": {*visited, data_id},
        }
        prep_method = cls._prep_unknown
        if isinstance(data, str):
            prep_method = cls._prep_string
        elif isinstance(data, Number):
            prep_method = cls._prep_number
        elif isinstance(data, (set, frozenset)):
            prep_method = cls._prep_set
        elif isinstance(data, (dict, MappingProxyType)):
            prep_method = cls._prep_dict
        elif cls.__is_namedtuple(data):
            prep_method = cls._prep_namedtuple
        elif isinstance(data, (list, tuple, GeneratorType)):
            prep_method = cls._prep_iterable
        return prep_method(**prep_kwargs)

    @classmethod
    def _serialize(
        cls,
        data: "PreppedValue",
        *,
        depth: int = 0,
    ) -> str:
        if isinstance(data, (str,)) or data is None:
            return str(data)
        serialize_method = cls.serialize_iterable
        if issubclass(data.value_type, str):
            serialize_method = cls.serialize_string
        elif issubclass(data.value_type, Number):
            serialize_method = cls.serialize_number
        return serialize_method(data=data, depth=depth)

    @classmethod
    def serialize_number(
        cls, data: "PreppedData", *, depth: int = 0, **kwargs: Any
    ) -> str:
        return cls.with_indent(str(data.value), depth=depth)

    @classmethod
    def serialize_string(
        cls, data: "PreppedData", *, depth: int = 0, **kwargs: Any
    ) -> str:
        if data.value is None:
            raise Exception("Attempting to serialize None as string")
        if isinstance(data.value, (str,)):
            return cls.with_indent(str(data.value), depth=depth)

        return cls.__serialize_lines(
            lines=(
                cls.with_indent(str(line.value), depth + 1 if depth else depth)
                for line in data.value
            ),
            depth=depth,
            open_tag="'''",
            close_tag="'''",
            ends="",
        )

    @classmethod
    def serialize_iterable(
        cls, data: "PreppedData", *, depth: int = 0, **kwargs: Any
    ) -> str:
        if isinstance(data.value, (str,)) or data.value is None:
            return cls.with_indent(str(data.value), depth=depth)

        open_paren, close_paren, separator, serialize_key = (None, None, None, False)
        if issubclass(data.value_type, list):
            open_paren, close_paren = ("[", "]")
        elif issubclass(data.value_type, (set, frozenset)):
            open_paren, close_paren = ("{", "}")
        elif issubclass(data.value_type, dict):
            open_paren, close_paren, separator, serialize_key = ("{", "}", ": ", True)
        elif issubclass(data.value_type, tuple) and data.value_type == tuple:
            pass
        else:
            separator = "="

        return cls.__serialize_iterable(
            data=data,
            open_paren=open_paren,
            close_paren=close_paren,
            depth=depth,
            separator=separator,
            serialize_key=serialize_key,
            **kwargs,
        )

    @classmethod
    def with_indent(cls, string: str, depth: int) -> str:
        return f"{cls._indent * depth}{string}"

    @classmethod
    def sort(
        cls,
        iterable: Iterable[Any],
        *,
        key: Optional[Callable[[Any], "SupportsRichComparison"]] = None,
    ) -> Iterable[Any]:
        try:
            return sorted(iterable)
        except TypeError:
            return sorted(iterable, key=(key or cls.serialize))

    @classmethod
    def object_type(cls, data: "SerializableData") -> str:
        return f"{data.__class__.__name__}"

    @classmethod
    def __is_namedtuple(cls, obj: Any) -> bool:
        return isinstance(obj, tuple) and all(
            type(n) == str for n in getattr(obj, "_fields", [None])
        )

    @classmethod
    def __serialize_iterable(
        cls,
        *,
        data: "PreppedData",
        open_paren: Optional[str] = None,
        close_paren: Optional[str] = None,
        depth: int = 0,
        separator: Optional[str] = None,
        serialize_key: bool = False,
        **kwargs: Any,
    ) -> str:
        kwargs["depth"] = depth + 1

        def key_str(key: Optional[Hashable]) -> str:
            if separator is None:
                return ""
            return (
                cls._serialize(
                    data=cls._prepare(key, **kwargs),
                    **kwargs,
                )
                if serialize_key
                else cls.with_indent(str(key), depth=kwargs["depth"])
            ) + separator

        def value_str(value: "PreppedValue") -> str:
            serialized = cls._serialize(data=value, **kwargs)
            return serialized if separator is None else serialized.lstrip(cls._indent)

        if not data or not data.value or isinstance(data.value, str):
            raise Exception(f"Attempting to serialize non iterable: {data.value}")

        return cls.__serialize_lines(
            lines=(f"{key_str(item.key)}{value_str(item)}," for item in data.value),
            depth=depth,
            open_tag=f"({open_paren or ''}",
            close_tag=f"{close_paren or ''})",
            obj_type=data.value_type.__name__,
        )

    @classmethod
    def __serialize_lines(
        cls,
        *,
        lines: Iterable[str],
        open_tag: str,
        close_tag: str,
        depth: int = 0,
        obj_type: Optional[str] = None,
        ends: str = "\n",
    ) -> str:
        lines = ends.join(lines)
        lines_end = "\n" if lines else ""
        maybe_obj_type = f"{obj_type}" if obj_type else ""
        formatted_open_tag = cls.with_indent(f"{maybe_obj_type}{open_tag}", depth)
        formatted_close_tag = cls.with_indent(close_tag, depth)
        return f"{formatted_open_tag}\n{lines}{lines_end}{formatted_close_tag}"

    @classmethod
    def _prep_number(self, data: Number, **kwargs: Any) -> "PreppedData":
        return PreppedData(value_type=type(data), value=str(data))

    @classmethod
    def _prep_string(self, data: str, **kwargs: Any) -> "PreppedData":
        if all(c not in data for c in self._marker_crn):
            return PreppedData(value_type=str, value=repr(data))

        return PreppedData(
            value_type=str,
            value=(
                PreppedData(
                    value_type=str,
                    value=line,
                )
                for line in str(data).splitlines(keepends=True)
            ),
        )

    @classmethod
    def _prep_iterable(
        cls, data: Iterable["SerializableData"], **kwargs: Any
    ) -> "PreppedData":
        values = list(data)
        return cls.__prep_iterable(
            data=data,
            resolve_entries=(range(len(values)), item_getter, None),
            include_keys=False,
            **kwargs,
        )

    @classmethod
    def _prep_set(cls, data: Set["SerializableData"], **kwargs: Any) -> "PreppedData":
        return cls.__prep_iterable(
            data=data,
            resolve_entries=(cls.sort(data), lambda _, p: p, None),
            include_keys=False,
            **kwargs,
        )

    @classmethod
    def _prep_namedtuple(cls, data: NamedTuple, **kwargs: Any) -> "PreppedData":
        return cls.__prep_iterable(
            data=data,
            resolve_entries=(cls.sort(data._fields), attr_getter, None),
            **kwargs,
        )

    @classmethod
    def _prep_dict(
        cls, data: Dict["PropertyName", "SerializableData"], **kwargs: Any
    ) -> "PreppedData":
        return cls.__prep_iterable(
            data=data,
            resolve_entries=(cls.sort(data.keys()), item_getter, None),
            **kwargs,
        )

    @classmethod
    def _prep_unknown(cls, data: Any, **kwargs: Any) -> "PreppedData":
        if data.__class__.__repr__ != object.__repr__:
            return PreppedData(value_type=type(data), value=repr(data))

        return cls.__prep_iterable(
            data=data,
            resolve_entries=(
                (name for name in cls.sort(dir(data)) if not name.startswith("_")),
                attr_getter,
                lambda v: not callable(v),
            ),
            **kwargs,
        )

    @classmethod
    def __prep_iterable(
        cls,
        *,
        data: "SerializableData",
        resolve_entries: "IterableEntries",
        depth: int = 0,
        exclude: Optional["PropertyFilter"] = None,
        path: "PropertyPath" = (),
        include_keys: bool = False,
        **kwargs: Any,
    ) -> "PreppedData":
        kwargs["depth"] = depth + 1

        keys, get_value, include_value = resolve_entries
        key_values = (
            (key, get_value(data, key))
            for key in keys
            if not exclude or not exclude(prop=key, path=path)
        )
        return PreppedData(
            value_type=type(data),
            value=(
                cls._prepare(
                    data=value,
                    exclude=exclude,
                    path=(*path, (key, type(value))),
                    **kwargs,
                ).with_key(None if include_keys else key)
                for key, value in key_values
                if not include_value or include_value(value)
            ),
        )
