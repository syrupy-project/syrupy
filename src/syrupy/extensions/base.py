import os
import warnings
from abc import (
    ABC,
    abstractmethod,
)
from difflib import ndiff
from itertools import zip_longest
from typing import (
    TYPE_CHECKING,
    Callable,
    Generator,
    Optional,
    Set,
    Union,
)

from typing_extensions import final

from syrupy.constants import SNAPSHOT_DIRNAME
from syrupy.data import (
    Snapshot,
    SnapshotEmptyFossil,
    SnapshotFossil,
    SnapshotFossils,
)
from syrupy.exceptions import SnapshotDoesNotExist
from syrupy.terminal import (
    emphasize,
    green,
    mute,
    red,
    reset,
)
from syrupy.utils import walk_snapshot_dir


if TYPE_CHECKING:
    from syrupy.location import TestLocation
    from syrupy.types import SerializableData, SerializedData


class SnapshotSerializer(ABC):
    @abstractmethod
    def serialize(self, data: "SerializableData") -> "SerializedData":
        """
        Serializes a python object / data structure into a string
        to be used for comparison with snapshot data from disk.
        """
        raise NotImplementedError


class SnapshotFossilizer(ABC):
    @property
    @abstractmethod
    def test_location(self) -> "TestLocation":
        raise NotImplementedError

    def get_snapshot_name(self, *, index: int = 0) -> str:
        """Get the snapshot name for the assertion index in a test location"""
        index_suffix = f".{index}" if index > 0 else ""
        testname = self.test_location.testname

        if self.test_location.classname is not None:
            return f"{self.test_location.classname}.{testname}{index_suffix}"
        return f"{testname}{index_suffix}"

    def get_location(self, *, index: int) -> str:
        """Returns full location where snapshot data is stored."""
        basename = self._get_file_basename(index=index)
        return os.path.join(self._dirname, f"{basename}.{self._file_extension}")

    def is_snapshot_location(self, *, location: str) -> bool:
        """Checks if supplied location is valid for this snapshot extension"""
        return location.endswith(self._file_extension)

    def discover_snapshots(self) -> "SnapshotFossils":
        """
        Returns all snapshot fossils in test site
        """
        discovered: "SnapshotFossils" = SnapshotFossils()
        for filepath in walk_snapshot_dir(self._dirname):
            if self.is_snapshot_location(location=filepath):
                snapshot_fossil = self._read_snapshot_fossil(snapshot_location=filepath)
                if not snapshot_fossil.has_snapshots:
                    snapshot_fossil = SnapshotEmptyFossil(location=filepath)
            else:
                snapshot_fossil = SnapshotFossil(location=filepath)
            discovered.add(snapshot_fossil)
        return discovered

    @final
    def read_snapshot(self, *, index: int) -> "SerializedData":
        """
        Utility method for reading the contents of a snapshot assertion.
        Will call `_pre_read`, then perform `read` and finally `post_read`,
        returning the contents parsed from the `read` method.

        Override `_read_snapshot_data_from_location` in subclass to change behaviour
        """
        try:
            self._pre_read(index=index)
            snapshot_location = self.get_location(index=index)
            snapshot_name = self.get_snapshot_name(index=index)
            snapshot_data = self._read_snapshot_data_from_location(
                snapshot_location=snapshot_location, snapshot_name=snapshot_name
            )
            if snapshot_data is None:
                raise SnapshotDoesNotExist()
            return snapshot_data
        finally:
            self._post_read(index=index)

    @final
    def write_snapshot(self, *, data: "SerializedData", index: int) -> None:
        """
        Utility method for writing the contents of a snapshot assertion.
        Will call `_pre_write`, then perform `write` and finally `_post_write`.

        Override `_write_snapshot_fossil` in subclass to change behaviour
        """
        self._pre_write(data=data, index=index)
        snapshot_location = self.get_location(index=index)
        snapshot_name = self.get_snapshot_name(index=index)
        if not self.test_location.matches_snapshot_name(snapshot_name):
            warning_msg = f"""
            Can not relate snapshot name '{snapshot_name}' to the test location.
            Consider adding '{self.test_location.testname}' to the generated name.
            """
            warnings.warn(warning_msg)
        snapshot_fossil = SnapshotFossil(location=snapshot_location)
        snapshot_fossil.add(Snapshot(name=snapshot_name, data=data))
        self._write_snapshot_fossil(snapshot_fossil=snapshot_fossil)
        self._post_write(data=data, index=index)

    @abstractmethod
    def delete_snapshots(
        self, *, snapshot_location: str, snapshot_names: Set[str]
    ) -> None:
        """
        Remove snapshots from a snapshot file.
        If the snapshot file will be empty remove the entire file.
        """
        raise NotImplementedError

    def _pre_read(self, *, index: int = 0) -> None:
        pass

    def _post_read(self, *, index: int = 0) -> None:
        pass

    def _pre_write(self, *, data: "SerializedData", index: int = 0) -> None:
        self.__ensure_snapshot_dir(index=index)

    def _post_write(self, *, data: "SerializedData", index: int = 0) -> None:
        pass

    @abstractmethod
    def _read_snapshot_fossil(self, *, snapshot_location: str) -> "SnapshotFossil":
        """
        Read the snapshot location and construct a snapshot fossil object
        """
        raise NotImplementedError

    @abstractmethod
    def _read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str
    ) -> Optional["SerializedData"]:
        """
        Get only the snapshot data from location for assertion
        """
        raise NotImplementedError

    @abstractmethod
    def _write_snapshot_fossil(self, *, snapshot_fossil: "SnapshotFossil") -> None:
        """
        Adds the snapshot data to the snapshots in fossil location
        """
        raise NotImplementedError

    @property
    def _dirname(self) -> str:
        test_dirname = os.path.dirname(self.test_location.filename)
        return os.path.join(test_dirname, SNAPSHOT_DIRNAME)

    @property
    @abstractmethod
    def _file_extension(self) -> str:
        raise NotImplementedError

    def _get_file_basename(self, *, index: int) -> str:
        """Returns file basename without extension. Used to create full filepath."""
        return f"{os.path.splitext(os.path.basename(self.test_location.filename))[0]}"

    def __ensure_snapshot_dir(self, *, index: int) -> None:
        """
        Ensures the folder path for the snapshot file exists.
        """
        try:
            os.makedirs(os.path.dirname(self.get_location(index=index)))
        except FileExistsError:
            pass


class SnapshotReporter(ABC):
    def diff_lines(
        self, serialized_data: "SerializedData", snapshot_data: "SerializedData"
    ) -> Generator[str, None, None]:
        for line in self.__diff_lines(str(snapshot_data), str(serialized_data)):
            yield reset(line)

    def __diff_lines(self, a: str, b: str) -> Generator[str, None, None]:
        line_styler = {"-": green, "+": red}
        staged_line, skip = "", False
        for line in ndiff(a.splitlines(), b.splitlines()):
            if staged_line and line[:1] != "?":
                yield line_styler[staged_line[:1]](staged_line)
                staged_line, skip = "", False
            if line[:1] in "-+":
                staged_line = line
            elif line[:1] == "?":
                yield self.__diff_line(line, staged_line, line_styler[staged_line[:1]])
                staged_line, skip = "", False
            elif not skip:
                yield mute("  ...")
                skip = True
        if staged_line:
            yield line_styler[staged_line[:1]](staged_line)

    def __diff_line(
        self, marker_line: str, line: str, line_style: Callable[[Union[str, int]], str]
    ) -> str:
        return "".join(
            emphasize(line_style(char)) if str(marker) in "-+^" else line_style(char)
            for marker, char in zip_longest(marker_line.strip(), line)
        )


class AbstractSyrupyExtension(SnapshotSerializer, SnapshotFossilizer, SnapshotReporter):
    def __init__(self, test_location: "TestLocation"):
        self._test_location = test_location

    @property
    def test_location(self) -> "TestLocation":
        return self._test_location
