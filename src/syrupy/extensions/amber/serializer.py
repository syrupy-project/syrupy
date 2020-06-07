from types import GeneratorType
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Optional,
    Set,
    Tuple,
)

from syrupy.constants import SYMBOL_ELLIPSIS
from syrupy.data import (
    Snapshot,
    SnapshotFossil,
)


if TYPE_CHECKING:
    from syrupy.types import (
        PropertyMatcher,
        PropertyName,
        PropertyPath,
        SerializableData,
    )


class Repr:
    def __init__(self, _repr: str):
        self._repr = _repr

    def __repr__(self) -> str:
        return self._repr


class DataSerializer:
    _indent: str = "  "
    _max_depth: int = 99
    _marker_divider: str = "---"
    _marker_name: str = "# name:"

    @classmethod
    def write_file(cls, snapshot_fossil: "SnapshotFossil") -> None:
        """
        Writes the snapshot data into the snapshot file that be read later.
        """
        filepath = snapshot_fossil.location
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            for snapshot in sorted(snapshot_fossil, key=lambda s: s.name):
                snapshot_data = str(snapshot.data)
                if snapshot_data is not None:
                    f.write(f"{cls._marker_name} {snapshot.name}\n")
                    for data_line in snapshot_data.splitlines(keepends=True):
                        f.write(f"{cls._indent}{data_line}")
                    f.write(f"\n{cls._marker_divider}\n")

    @classmethod
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
            with open(filepath, "r", encoding="utf-8", newline="") as f:
                test_name = None
                snapshot_data = ""
                for line in f:
                    if line.startswith(cls._marker_name):
                        test_name = line[name_marker_len:-1].strip(" \r\n")
                        snapshot_data = ""
                        continue
                    elif test_name is not None:
                        if line.startswith(cls._indent):
                            snapshot_data += line[indent_len:]
                        elif line.startswith(cls._marker_divider) and snapshot_data:
                            snapshot_fossil.add(
                                Snapshot(name=test_name, data=snapshot_data[:-1])
                            )
        except FileNotFoundError:
            pass

        return snapshot_fossil

    @classmethod
    def serialize(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: Optional[Set[Any]] = None,
    ) -> str:
        visited = set() if visited is None else visited
        data_id = id(data)
        if depth > cls._max_depth or data_id in visited:
            data = Repr(SYMBOL_ELLIPSIS)
        elif matcher:
            data = matcher(data=data, path=path)
        serialize_kwargs = {
            "data": data,
            "depth": depth,
            "matcher": matcher,
            "path": path,
            "visited": {*visited, data_id},
        }
        serialize_method = cls.serialize_unknown
        if isinstance(data, str):
            serialize_method = cls.serialize_string
        elif isinstance(data, (int, float)):
            serialize_method = cls.serialize_number
        elif isinstance(data, (set, frozenset)):
            serialize_method = cls.serialize_set
        elif isinstance(data, dict):
            serialize_method = cls.serialize_dict
        elif cls.__is_namedtuple(data):
            serialize_method = cls.serialize_namedtuple
        elif isinstance(data, (list, tuple, GeneratorType)):
            serialize_method = cls.serialize_iterable
        return serialize_method(**serialize_kwargs)

    @classmethod
    def serialize_number(
        cls, data: "SerializableData", *, depth: int = 0, **kwargs: Any
    ) -> str:
        return cls.with_indent(repr(data), depth)

    @classmethod
    def serialize_string(
        cls, data: "SerializableData", *, depth: int = 0, **kwargs: Any
    ) -> str:
        if "\n" in data:
            return cls.__serialize_lines(
                data=data,
                lines=(
                    cls.with_indent(line, depth + 1 if depth else depth)
                    for line in str(data).splitlines(keepends=True)
                ),
                depth=depth,
                open_tag="'",
                close_tag="'",
                include_type=False,
                ends="",
            )
        return cls.with_indent(repr(data), depth)

    @classmethod
    def serialize_iterable(cls, data: "SerializableData", **kwargs: Any) -> str:
        open_paren, close_paren = next(
            parens
            for iter_type, parens in {
                GeneratorType: ("(", ")"),
                list: ("[", "]"),
                tuple: ("(", ")"),
            }.items()
            if isinstance(data, iter_type)
        )
        return cls.__serialize_iterable(
            data=data,
            entries=enumerate(data),
            open_tag=open_paren,
            close_tag=close_paren,
            **kwargs,
        )

    @classmethod
    def serialize_set(cls, data: "SerializableData", **kwargs: Any) -> str:
        return cls.__serialize_iterable(
            data=data,
            entries=((d, d) for d in cls.sort(data)),
            open_tag="{",
            close_tag="}",
            **kwargs,
        )

    @classmethod
    def serialize_namedtuple(cls, data: "SerializableData", **kwargs: Any) -> str:
        return cls.__serialize_iterable(
            data=data,
            entries=((name, getattr(data, name)) for name in cls.sort(data._fields)),
            open_tag="(",
            close_tag=")",
            separator="=",
            **kwargs,
        )

    @classmethod
    def serialize_dict(cls, data: "SerializableData", **kwargs: Any) -> str:
        return cls.__serialize_iterable(
            data=data,
            entries=((key, data[key]) for key in cls.sort(data.keys())),
            open_tag="{",
            close_tag="}",
            separator=": ",
            serialize_key=True,
            **kwargs,
        )

    @classmethod
    def serialize_unknown(cls, data: Any, *, depth: int = 0, **kwargs: Any) -> str:
        if data.__class__.__repr__ != object.__repr__:
            return cls.with_indent(repr(data), depth)

        return cls.__serialize_iterable(
            data=data,
            entries=(
                (name, getattr(data, name))
                for name in cls.sort(dir(data))
                if not name.startswith("_") and not callable(getattr(data, name))
            ),
            depth=depth,
            open_tag="{",
            close_tag="}",
            separator="=",
            **kwargs,
        )

    @classmethod
    def with_indent(cls, string: str, depth: int) -> str:
        return f"{cls._indent * depth}{string}"

    @classmethod
    def sort(cls, iterable: Iterable[Any]) -> Iterable[Any]:
        try:
            return sorted(iterable)
        except TypeError:
            return sorted(iterable, key=cls.serialize)

    @classmethod
    def object_type(cls, data: "SerializableData") -> str:
        return f"<class '{data.__class__.__name__}'>"

    @classmethod
    def __is_namedtuple(cls, obj: Any) -> bool:
        return isinstance(obj, tuple) and all(
            type(n) == str for n in getattr(obj, "_fields", [None])
        )

    @classmethod
    def __serialize_lines(
        cls,
        *,
        data: "SerializableData",
        lines: Iterable[str],
        open_tag: str,
        close_tag: str,
        depth: int = 0,
        include_type: bool = True,
        ends: str = "\n",
    ) -> str:
        return (
            f"{cls.with_indent(cls.object_type(data), depth)} " if include_type else ""
        ) + f"{open_tag}\n{ends.join(lines)}\n{cls.with_indent(close_tag, depth)}"

    @classmethod
    def __serialize_iterable(
        cls,
        *,
        data: "SerializableData",
        entries: Iterable[Tuple["PropertyName", "SerializableData"]],
        open_tag: str,
        close_tag: str,
        depth: int = 0,
        path: "PropertyPath" = (),
        separator: Optional[str] = None,
        serialize_key: bool = False,
        **kwargs: Any,
    ) -> str:
        kwargs["depth"] = depth + 1

        def key_str(key: "PropertyName") -> str:
            if separator is None:
                return ""
            return (
                cls.serialize(data=key, **kwargs)
                if serialize_key
                else cls.with_indent(str(key), depth=depth + 1)
            ) + separator

        def value_str(key: "PropertyName", value: "SerializableData") -> str:
            _path = (*path, (key, type(value)))
            serialized = cls.serialize(data=value, path=_path, **kwargs)
            return serialized if separator is None else serialized.lstrip(cls._indent)

        return cls.__serialize_lines(
            data=data,
            lines=(f"{key_str(key)}{value_str(key, value)}," for key, value in entries),
            depth=depth,
            open_tag=open_tag,
            close_tag=close_tag,
        )
