import os
from types import GeneratorType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Set,
)

from .base import AbstractSnapshotSerializer


if TYPE_CHECKING:
    from syrupy.types import SerializableData


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
        return "snap"

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

    def __with_indent(self, string: str, indent: int) -> str:
        return f"{self.__indent * indent}{string}"

    def __serialize(self, data: "SerializableData", indent: int = 0) -> str:
        if isinstance(data, str):
            if "\n" in data:
                return (
                    self.__with_indent("'\n", indent)
                    + str(data)
                    + self.__with_indent("\n'", indent)
                )
            return self.__with_indent(repr(data), indent)

        if isinstance(data, (int, float)):
            return self.__with_indent(repr(data), indent)

        if isinstance(data, set):
            return (
                self.__with_indent(f"{type(data)} {{\n", indent)
                + "".join(
                    [f"{self.__serialize(d, indent + 1)},\n" for d in sorted(data)]
                )
                + self.__with_indent("}", indent)
            )

        if isinstance(data, dict):
            return (
                self.__with_indent(f"{type(data)} {{\n", indent)
                + "".join(
                    [
                        (
                            self.__serialize(key, indent + 1)
                            + ": "
                            + self.__serialize(data[key], indent + 1).lstrip(
                                self.__indent
                            )
                            + ",\n"
                        )
                        for key in sorted(data.keys())
                    ]
                )
                + self.__with_indent("}", indent)
            )

        if isinstance(data, (list, tuple, GeneratorType)):
            open_paren, close_paren = next(
                paren[1]
                for paren in {list: "[]", tuple: "()", GeneratorType: "()"}.items()
                if isinstance(data, paren[0])
            )
            return (
                self.__with_indent(f"{type(data)} {open_paren}\n", indent)
                + "".join([f"{self.__serialize(d, indent + 1)},\n" for d in data])
                + self.__with_indent(close_paren, indent)
            )

        return self.__with_indent(repr(data), indent)

    def serialize(self, data: "SerializableData") -> str:
        """
        Returns the serialized form of 'data' to be compared
        with the snapshot data written to disk.
        """
        return self.__serialize(data)

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
                    if test_name is None:
                        continue
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
