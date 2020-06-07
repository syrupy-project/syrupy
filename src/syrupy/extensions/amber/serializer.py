from types import GeneratorType
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Optional,
    Set,
)

from syrupy.constants import SYMBOL_ELLIPSIS
from syrupy.data import (
    Snapshot,
    SnapshotFossil,
)


if TYPE_CHECKING:
    from syrupy.types import (
        PropertyMatcher,
        PropertyPath,
        SerializableData,
    )


class DataSerializer:
    _indent: str = "  "
    _max_depth: int = 99
    _marker_divider: str = "---"
    _marker_name: str = "# name:"

    class MarkerDepthMax:
        def __repr__(self) -> str:
            return SYMBOL_ELLIPSIS

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
    def sort(cls, iterable: Iterable[Any]) -> Iterable[Any]:
        try:
            return sorted(iterable)
        except TypeError:
            return sorted(iterable, key=cls.serialize)

    @classmethod
    def with_indent(cls, string: str, depth: int) -> str:
        return f"{cls._indent * depth}{string}"

    @classmethod
    def object_type(cls, data: "SerializableData") -> str:
        return f"<class '{data.__class__.__name__}'>"

    @classmethod
    def serialize_string(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: Optional[Set[Any]] = None,
    ) -> str:
        if "\n" in data:
            return (
                cls.with_indent("'\n", depth)
                + "".join(
                    cls.with_indent(line, depth + 1 if depth else depth)
                    for line in str(data).splitlines(keepends=True)
                )
                + "\n"
                + cls.with_indent("'", depth)
            )
        return cls.with_indent(repr(data), depth)

    @classmethod
    def serialize_number(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: Optional[Set[Any]] = None,
    ) -> str:
        return cls.with_indent(repr(data), depth)

    @classmethod
    def serialize_set(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: Optional[Set[Any]] = None,
    ) -> str:
        return (
            cls.with_indent(f"{cls.object_type(data)} {{\n", depth)
            + "".join(
                cls.serialize(
                    data=d,
                    depth=depth + 1,
                    matcher=matcher,
                    path=(*path, (d, type(d))),
                    visited=visited,
                )
                + ",\n"
                for d in cls.sort(data)
            )
            + cls.with_indent("}", depth)
        )

    @classmethod
    def serialize_dict(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: Optional[Set[Any]] = None,
    ) -> str:
        kwargs = {"depth": depth + 1, "matcher": matcher, "visited": visited}
        return (
            cls.with_indent(f"{cls.object_type(data)} {{\n", depth)
            + "".join(
                f"{serialized_key}: {serialized_value.lstrip(cls._indent)},\n"
                for serialized_key, serialized_value in (
                    (
                        cls.serialize(**{"data": key, **kwargs}),
                        cls.serialize(
                            **{
                                "data": data[key],
                                "path": (*path, (key, type(data[key]))),
                                **kwargs,
                            }
                        ),
                    )
                    for key in cls.sort(data.keys())
                )
            )
            + cls.with_indent("}", depth)
        )

    @classmethod
    def __is_namedtuple(cls, obj: Any) -> bool:
        return isinstance(obj, tuple) and all(
            type(n) == str for n in getattr(obj, "_fields", [None])
        )

    @classmethod
    def serialize_namedtuple(
        cls,
        data: Any,
        *,
        depth: int = 0,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: Optional[Set[Any]] = None,
    ) -> str:
        return (
            cls.with_indent(f"{cls.object_type(data)} (\n", depth)
            + "".join(
                f"{serialized_key}={serialized_value.lstrip(cls._indent)},\n"
                for serialized_key, serialized_value in (
                    (
                        cls.with_indent(name, depth=depth + 1),
                        cls.serialize(
                            data=getattr(data, name),
                            depth=depth + 1,
                            matcher=matcher,
                            path=(*path, (name, type(getattr(data, name)))),
                            visited=visited,
                        ),
                    )
                    for name in cls.sort(data._fields)
                )
            )
            + cls.with_indent(")", depth)
        )

    @classmethod
    def serialize_iterable(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: Optional[Set[Any]] = None,
    ) -> str:
        open_paren, close_paren = next(
            parens
            for iter_type, parens in {
                GeneratorType: ("(", ")"),
                list: ("[", "]"),
                tuple: ("(", ")"),
            }.items()
            if isinstance(data, iter_type)
        )
        return (
            cls.with_indent(f"{cls.object_type(data)} {open_paren}\n", depth)
            + "".join(
                cls.serialize(
                    data=d,
                    depth=depth + 1,
                    matcher=matcher,
                    path=(*path, (i, type(d))),
                    visited=visited,
                )
                + ",\n"
                for i, d in enumerate(data)
            )
            + cls.with_indent(close_paren, depth)
        )

    @classmethod
    def serialize_unknown(
        cls,
        data: Any,
        *,
        depth: int = 0,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: Optional[Set[Any]] = None,
    ) -> str:
        if data.__class__.__repr__ != object.__repr__:
            return cls.with_indent(repr(data), depth)

        return (
            cls.with_indent(f"{cls.object_type(data)} {{\n", depth)
            + "".join(
                f"{serialized_key}={serialized_value.lstrip(cls._indent)},\n"
                for serialized_key, serialized_value in (
                    (
                        cls.with_indent(name, depth=depth + 1),
                        cls.serialize(
                            data=getattr(data, name),
                            depth=depth + 1,
                            matcher=matcher,
                            path=(*path, (name, type(getattr(data, name)))),
                            visited=visited,
                        ),
                    )
                    for name in cls.sort(dir(data))
                    if not name.startswith("_") and not callable(getattr(data, name))
                )
            )
            + cls.with_indent("}", depth)
        )

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
        visited = visited if visited is not None else set()
        data_id = id(data)
        if depth > cls._max_depth or data_id in visited:
            data = cls.MarkerDepthMax()
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
