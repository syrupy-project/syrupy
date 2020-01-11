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
    SnapshotEmptyFile,
    SnapshotFile,
    SnapshotFiles,
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


class SnapshotCacher(ABC):
    @property
    def test_location(self) -> "TestLocation":
        raise NotImplementedError

    @final
    def read_snapshot(self, index: int) -> "SerializedData":
        """
        Utility method for reading the contents of a snapshot assertion.
        Will call `pre_read`, then `read` and finally `post_read`,
        returning the contents parsed from the `read` method.
        """
        try:
            self.pre_read(index=index)
            return self.read(index=index)
        finally:
            self.post_read(index=index)

    @final
    def create_or_update_snapshot(self, data: "SerializedData", index: int) -> None:
        """
        Utility method for writing the contents of a snapshot assertion.
        Will call `pre_write`, then `write` and finally `post_write`.
        """
        self.pre_write(data, index=index)
        self.write(data, index=index)
        self.post_write(data, index=index)

    @abstractmethod
    def delete_snapshots_from_file(
        self, snapshot_filepath: str, snapshot_names: Set[str]
    ) -> None:
        """
        Remove snapshots from a snapshot file.
        If the snapshot file will be empty remove the entire file.
        """
        raise NotImplementedError

    def pre_read(self, index: int = 0) -> None:
        pass

    @final
    def read(self, index: int = 0) -> "SerializedData":
        """
        Override `_read_snapshot_from_file` in subclass to change behaviour
        """
        snapshot_file = self.get_filepath(index)
        snapshot_name = self.get_snapshot_name(index)
        snapshot = self._read_snapshot_from_file(snapshot_file, snapshot_name)
        if snapshot is None:
            raise SnapshotDoesNotExist()
        return snapshot

    def post_read(self, index: int = 0) -> None:
        pass

    def pre_write(self, data: "SerializedData", index: int = 0) -> None:
        self.__ensure_snapshot_dir(index)

    @final
    def write(self, data: "SerializedData", index: int = 0) -> None:
        """
        Override `_write_snapshot_to_file` in subclass to change behaviour
        """
        snapshot_filepath = self.get_filepath(index)
        snapshot_name = self.get_snapshot_name(index)
        if not self.test_location.matches_snapshot_name(snapshot_name):
            warning_msg = f"""
            Can not relate snapshot name '{snapshot_name}' to the test location.
            Consider adding '{self.test_location.testname}' to the generated name.
            """
            warnings.warn(warning_msg)
        snapshot_file = SnapshotFile(filepath=snapshot_filepath)
        snapshot_file.add(Snapshot(name=snapshot_name, data=data))
        self._write_snapshot_to_file(snapshot_file)

    def post_write(self, data: "SerializedData", index: int = 0) -> None:
        pass

    def get_filepath(self, index: int) -> str:
        """Returns full filepath where snapshot data is stored."""
        basename = self.get_file_basename(index=index)
        return os.path.join(self.dirname, f"{basename}.{self.file_extension}")

    def get_file_basename(self, index: int) -> str:
        """Returns file basename without extension. Used to create full filepath."""
        return f"{os.path.splitext(os.path.basename(self.test_location.filename))[0]}"

    def __ensure_snapshot_dir(self, index: int) -> None:
        """
        Ensures the folder path for the snapshot file exists.
        """
        try:
            os.makedirs(os.path.dirname(self.get_filepath(index)))
        except FileExistsError:
            pass

    @property
    @abstractmethod
    def file_extension(self) -> str:
        raise NotImplementedError

    @property
    def dirname(self) -> str:
        test_dirname = os.path.dirname(self.test_location.filename)
        subdir_name = self.snapshot_subdirectory_name
        if subdir_name is not None:
            return os.path.join(test_dirname, SNAPSHOT_DIRNAME, subdir_name)
        return os.path.join(test_dirname, SNAPSHOT_DIRNAME)

    @property
    def snapshot_subdirectory_name(self) -> Optional[str]:
        """Optional subdirectory in which to store snapshots."""
        return None

    def get_snapshot_name(self, index: int = 0) -> str:
        index_suffix = f".{index}" if index > 0 else ""
        testname = self.test_location.testname

        if self.test_location.classname is not None:
            return f"{self.test_location.classname}.{testname}{index_suffix}"
        return f"{testname}{index_suffix}"

    @abstractmethod
    def _read_snapshot_from_file(
        self, snapshot_filepath: str, snapshot_name: str
    ) -> Optional["SerializedData"]:
        """
        Read the snapshot file and get only the snapshot data for assertion
        """
        raise NotImplementedError

    @abstractmethod
    def _write_snapshot_to_file(self, snapshot_file: "SnapshotFile") -> None:
        """
        Adds the snapshot data to the snapshots read from the file
        """
        raise NotImplementedError


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


class AbstractSyrupyExtension(SnapshotSerializer, SnapshotCacher, SnapshotReporter):
    def __init__(self, test_location: "TestLocation"):
        self._test_location = test_location

    @property
    def test_location(self) -> "TestLocation":
        return self._test_location

    def discover_snapshots(self) -> "SnapshotFiles":
        """
        Returns all snapshot files relating to test location
        """
        discovered_files: "SnapshotFiles" = SnapshotFiles()
        for filepath in walk_snapshot_dir(self.dirname):
            if filepath.endswith(self.file_extension):
                snapshot_file = self._discover_snapshots(filepath)
                if not snapshot_file.has_snapshots:
                    snapshot_file = SnapshotEmptyFile(filepath=filepath)
            else:
                snapshot_file = SnapshotFile(filepath=filepath)
            discovered_files.add(snapshot_file)
        return discovered_files

    @abstractmethod
    def _discover_snapshots(self, snapshot_file: str) -> "SnapshotFile":
        """
        Given a path to a snapshot file, returns all snapshots in the file.
        Snapshot name is dependent on serializer implementation.
        """
        raise NotImplementedError
