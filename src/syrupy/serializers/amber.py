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
    indent: str = "  "

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
    def with_indent(cls, string: str, indent: int) -> str:
        return f"{cls.indent * indent}{string}"

    @classmethod
    def serialize_string(cls, data: "SerializableData", indent: int = 0) -> str:
        if "\n" in data:
            return (
                cls.with_indent("'\n", indent)
                + str(data)
                + cls.with_indent("\n'", indent)
            )
        return cls.with_indent(repr(data), indent)

    @classmethod
    def serialize_number(cls, data: "SerializableData", indent: int = 0) -> str:
        return cls.with_indent(repr(data), indent)

    @classmethod
    def serialize_set(cls, data: "SerializableData", indent: int = 0) -> str:
        return (
            cls.with_indent(f"{type(data)} {{\n", indent)
            + "".join([f"{cls.serialize(d, indent + 1)},\n" for d in cls.sort(data)])
            + cls.with_indent("}", indent)
        )

    @classmethod
    def serialize_dict(cls, data: "SerializableData", indent: int = 0) -> str:
        return (
            cls.with_indent(f"{type(data)} {{\n", indent)
            + "".join(
                [
                    (
                        cls.serialize(key, indent + 1)
                        + ": "
                        + cls.serialize(data[key], indent + 1).lstrip(cls.indent)
                        + ",\n"
                    )
                    for key in cls.sort(data.keys())
                ]
            )
            + cls.with_indent("}", indent)
        )

    @classmethod
    def serialize_iterable(cls, data: "SerializableData", indent: int = 0) -> str:
        open_paren, close_paren = next(
            paren[1]
            for paren in {list: "[]", tuple: "()", GeneratorType: "()"}.items()
            if isinstance(data, paren[0])
        )
        return (
            cls.with_indent(f"{type(data)} {open_paren}\n", indent)
            + "".join([f"{cls.serialize(d, indent + 1)},\n" for d in data])
            + cls.with_indent(close_paren, indent)
        )

    @classmethod
    def serialize(cls, data: "SerializableData", indent: int = 0) -> str:
        if isinstance(data, str):
            return cls.serialize_string(data, indent)
        elif isinstance(data, (int, float)):
            return cls.serialize_number(data, indent)
        elif isinstance(data, (set, frozenset)):
            return cls.serialize_set(data, indent)
        elif isinstance(data, dict):
            return cls.serialize_dict(data, indent)
        elif isinstance(data, (list, tuple, GeneratorType)):
            return cls.serialize_iterable(data, indent)
        return cls.with_indent(repr(data), indent)


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
        return set(name for name in self.__read_file(filepath).keys())

    def _read_snapshot_from_file(
        self, snapshot_file: str, snapshot_name: str
    ) -> "SerializableData":
        snapshots = self.__read_file(snapshot_file)
        return snapshots.get(snapshot_name, {}).get("data")

    def _write_snapshot_to_file(
        self, snapshot_file: str, snapshot_name: str, data: "SerializableData"
    ) -> None:
        snapshots = self.__read_file(snapshot_file)
        snapshots[snapshot_name] = {
            "data": self.serialize(data),
        }
        self.__write_file(snapshot_file, snapshots)

    def delete_snapshot_from_file(self, snapshot_file: str, snapshot_name: str) -> None:
        snapshots = self.__read_file(snapshot_file)
        if snapshot_name in snapshots:
            del snapshots[snapshot_name]

        if snapshots:
            self.__write_file(snapshot_file, snapshots)
        else:
            os.remove(snapshot_file)

    def serialize(self, data: "SerializableData") -> str:
        """
        Returns the serialized form of 'data' to be compared
        with the snapshot data written to disk.
        """
        return DataSerializer.serialize(data)

    def __write_file(self, filepath: str, snapshots: Dict[str, Dict[str, Any]]) -> None:
        """
        Writes the snapshot data into the snapshot file that be read later.
        """
        with open(filepath, "w") as f:
            for key in sorted(snapshots.keys()):
                snapshot = snapshots[key]
                snapshot_data = snapshot.get("data")
                if snapshot_data is not None:
                    f.write(f"{self.__name_marker} {key}\n")
                    for data_line in snapshot_data.split("\n"):
                        f.write(f"{self.__indent}{data_line}\n")
                    f.write(f"{self.__divider}\n")

    def __read_file(self, filepath: str) -> Dict[str, Dict[str, Any]]:
        """
        Read the raw snapshot data (str) from the snapshot file into a dict
        of snapshot name to raw data. This does not attempt any deserialization
        of the snapshot data.
        """
        name_marker_len = len(self.__name_marker)
        indent_len = len(self.__indent)
        snapshots = {}
        test_name = None
        snapshot_data = ""
        try:
            with open(filepath, "r") as f:
                for line in f:
                    if line.startswith(self.__name_marker):
                        test_name = line[name_marker_len:-1].strip(" \n")
                        snapshot_data = ""
                        continue
                    elif test_name is not None:
                        if line.startswith(self.__indent):
                            snapshot_data += line[indent_len:]
                        elif line.startswith(self.__divider) and snapshot_data:
                            snapshots[test_name] = {"data": snapshot_data[:-1]}
        except FileNotFoundError:
            pass

        return snapshots

    @property
    def __indent(self) -> str:
        return "  "

    @property
    def __name_marker(self) -> str:
        return "# name:"

    @property
    def __divider(self) -> str:
        return "---"
