import hashlib
import os
from types import GeneratorType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Set,
)

from .base import AbstractSnapshotSerializer


if TYPE_CHECKING:
    from syrupy.types import SerializableData


class DataSerializer:
    _indent: str = "  "
    _max_depth: int = 99
    _marker_divider: str = "---"
    _marker_name: str = "# name:"

    class MarkerDepthMax:
        def __repr__(self) -> str:
            return "..."

    @classmethod
    def write_file(cls, filepath: str, snapshots: Dict[str, Dict[str, Any]]) -> None:
        """
        Writes the snapshot data into the snapshot file that be read later.
        """
        with open(filepath, "w") as f:
            for key in sorted(snapshots.keys()):
                snapshot = snapshots[key]
                snapshot_data = snapshot.get("data")
                if snapshot_data is not None:
                    f.write(f"{cls._marker_name} {key}\n")
                    for data_line in snapshot_data.split("\n"):
                        f.write(f"{cls._indent}{data_line}\n")
                    f.write(f"{cls._marker_divider}\n")

    @classmethod
    def read_file(cls, filepath: str) -> Dict[str, Dict[str, Any]]:
        """
        Read the raw snapshot data (str) from the snapshot file into a dict
        of snapshot name to raw data. This does not attempt any deserialization
        of the snapshot data.
        """
        name_marker_len = len(cls._marker_name)
        indent_len = len(cls._indent)
        snapshots = {}
        test_name = None
        snapshot_data = ""
        try:
            with open(filepath, "r") as f:
                for line in f:
                    if line.startswith(cls._marker_name):
                        test_name = line[name_marker_len:-1].strip(" \n")
                        snapshot_data = ""
                        continue
                    elif test_name is not None:
                        if line.startswith(cls._indent):
                            snapshot_data += line[indent_len:]
                        elif line.startswith(cls._marker_divider) and snapshot_data:
                            snapshots[test_name] = {"data": snapshot_data[:-1]}
        except FileNotFoundError:
            pass

        return snapshots

    @classmethod
    def sort(cls, iterable: Iterable[Any]) -> Iterable[Any]:
        def _sort_key(value: Any) -> Any:
            if isinstance(value, frozenset):
                h = hashlib.sha256()
                for element in cls.sort(value):
                    h.update(str(element).encode("utf-8"))
                return h.hexdigest()
            return value

        try:
            return sorted(iterable)
        except TypeError:
            return sorted(iterable, key=_sort_key)

    @classmethod
    def with_indent(cls, string: str, depth: int) -> str:
        return f"{cls._indent * depth}{string}"

    @classmethod
    def object_type(cls, data: "SerializableData") -> str:
        return f"<class '{data.__class__.__name__}'>"

    @classmethod
    def serialize_string(
        cls, data: "SerializableData", *, depth: int = 0, visited: Set[Any] = set()
    ) -> str:
        if "\n" in data:
            return (
                cls.with_indent("'\n", depth)
                + str(data)
                + cls.with_indent("\n'", depth)
            )
        return cls.with_indent(repr(data), depth)

    @classmethod
    def serialize_number(
        cls, data: "SerializableData", *, depth: int = 0, visited: Set[Any] = set()
    ) -> str:
        return cls.with_indent(repr(data), depth)

    @classmethod
    def serialize_set(
        cls, data: "SerializableData", *, depth: int = 0, visited: Set[Any] = set()
    ) -> str:
        return (
            cls.with_indent(f"{cls.object_type(data)} {{\n", depth)
            + "".join(
                f"{cls.serialize(d, depth=depth + 1, visited=visited)},\n"
                for d in cls.sort(data)
            )
            + cls.with_indent("}", depth)
        )

    @classmethod
    def serialize_dict(
        cls, data: "SerializableData", *, depth: int = 0, visited: Set[Any] = set()
    ) -> str:
        kwargs = dict(depth=depth + 1, visited=visited)
        return (
            cls.with_indent(f"{cls.object_type(data)} {{\n", depth)
            + "".join(
                f"{serialized_key}: {serialized_value.lstrip(cls._indent)},\n"
                for serialized_key, serialized_value in (
                    (
                        cls.serialize(**dict(data=key, **kwargs)),
                        cls.serialize(**dict(data=data[key], **kwargs)),
                    )
                    for key in cls.sort(data.keys())
                )
            )
            + cls.with_indent("}", depth)
        )

    @classmethod
    def serialize_iterable(
        cls, data: "SerializableData", *, depth: int = 0, visited: Set[Any] = set()
    ) -> str:
        open_paren, close_paren = next(
            paren[1]
            for paren in {list: "[]", tuple: "()", GeneratorType: "()"}.items()
            if isinstance(data, paren[0])
        )
        return (
            cls.with_indent(f"{cls.object_type(data)} {open_paren}\n", depth)
            + "".join(
                f"{cls.serialize(d, depth=depth + 1, visited=visited)},\n" for d in data
            )
            + cls.with_indent(close_paren, depth)
        )

    @classmethod
    def serialize_unknown(
        cls, data: Any, *, depth: int = 0, visited: Set[Any] = set()
    ) -> str:
        return cls.with_indent(repr(data), depth)

    @classmethod
    def serialize(
        cls, data: "SerializableData", *, depth: int = 0, visited: Set[Any] = set()
    ) -> str:
        data_id = id(data)
        if depth > cls._max_depth or data_id in visited:
            data = cls.MarkerDepthMax()

        serialize_kwargs = dict(data=data, depth=depth, visited={*visited, data_id})
        serialize_method = cls.serialize_unknown
        if isinstance(data, str):
            serialize_method = cls.serialize_string
        elif isinstance(data, (int, float)):
            serialize_method = cls.serialize_number
        elif isinstance(data, (set, frozenset)):
            serialize_method = cls.serialize_set
        elif isinstance(data, dict):
            serialize_method = cls.serialize_dict
        elif isinstance(data, (list, tuple, GeneratorType)):
            serialize_method = cls.serialize_iterable
        return serialize_method(**serialize_kwargs)


class AmberSnapshotSerializer(AbstractSnapshotSerializer):
    """
    An amber snapshot file stores data in the following format:

    ```
    # name: test_name_1
      data
    ---
    # name: test_name_2
      data
    ```
    """

    @property
    def file_extension(self) -> str:
        return "ambr"

    def discover_snapshots(self, filepath: str) -> Set[str]:
        return set(name for name in DataSerializer.read_file(filepath).keys())

    def _read_snapshot_from_file(
        self, snapshot_file: str, snapshot_name: str
    ) -> "SerializableData":
        snapshots = DataSerializer.read_file(snapshot_file)
        return snapshots.get(snapshot_name, {}).get("data")

    def _write_snapshot_to_file(
        self, snapshot_file: str, snapshot_name: str, data: "SerializableData"
    ) -> None:
        snapshots = DataSerializer.read_file(snapshot_file)
        snapshots[snapshot_name] = {
            "data": self.serialize(data),
        }
        DataSerializer.write_file(snapshot_file, snapshots)

    def delete_snapshots_from_file(
        self, snapshot_file: str, snapshot_names: Set[str]
    ) -> None:
        snapshots = DataSerializer.read_file(snapshot_file)
        for snapshot_name in snapshot_names:
            snapshots.pop(snapshot_name, None)

        if snapshots:
            DataSerializer.write_file(snapshot_file, snapshots)
        else:
            os.remove(snapshot_file)

    def serialize(self, data: "SerializableData") -> str:
        """
        Returns the serialized form of 'data' to be compared
        with the snapshot data written to disk.
        """
        return DataSerializer.serialize(data)
