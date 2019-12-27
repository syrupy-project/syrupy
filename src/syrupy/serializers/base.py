import os
import warnings
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    TYPE_CHECKING,
    Optional,
    Set,
    Union,
)

from typing_extensions import final

from syrupy.constants import SNAPSHOT_DIRNAME
from syrupy.exceptions import SnapshotDoesNotExist


if TYPE_CHECKING:
    from syrupy.types import SerializableData
    from syrupy.location import TestLocation


class AbstractSnapshotSerializer(ABC):
    def __init__(self, test_location: "TestLocation"):
        self._test_location = test_location

    @property
    @abstractmethod
    def file_extension(self) -> str:
        raise NotImplementedError

    @property
    def test_location(self) -> "TestLocation":
        return self._test_location

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

    @abstractmethod
    def serialize(self, data: "SerializableData") -> Union[str, bytes]:
        """
        Serializes a python object / data structure into a string
        to be used for comparison with snapshot data from disk.
        """
        raise NotImplementedError

    @abstractmethod
    def discover_snapshots(self, filepath: str) -> Set[str]:
        """
        Given a snapshot file, returns a Set of all snapshots
        within the file. Snapshot name is dependent on serializer
        implementation.
        """
        raise NotImplementedError

    @final
    def read_snapshot(self, index: int) -> "SerializableData":
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
    def create_or_update_snapshot(self, data: "SerializableData", index: int) -> None:
        """
        Utility method for writing the contents of a snapshot assertion.
        Will call `pre_write`, then `write` and finally `post_write`.
        """
        self.pre_write(data, index=index)
        self.write(data, index=index)
        self.post_write(data, index=index)

    @abstractmethod
    def delete_snapshot_from_file(self, snapshot_file: str, snapshot_name: str) -> None:
        """
        Remove a snapshot from a snapshot file.
        If the snapshot file will be empty remove the entire file.
        """
        raise NotImplementedError

    def pre_read(self, index: int = 0) -> None:
        pass

    @final
    def read(self, index: int = 0) -> "SerializableData":
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

    def pre_write(self, data: "SerializableData", index: int = 0) -> None:
        self.__ensure_snapshot_dir(index)

    @final
    def write(self, data: "SerializableData", index: int = 0) -> None:
        """
        Override `_write_snapshot_to_file` in subclass to change behaviour
        """
        snapshot_file = self.get_filepath(index)
        snapshot_name = self.get_snapshot_name(index)
        if self.test_location.testname not in snapshot_name:
            warning_msg = (
                f"Snapshot name '{snapshot_name}' does not contain testname"
                f" '{self.test_location.testname}'"
            )
            warnings.warn(warning_msg)
        self._write_snapshot_to_file(snapshot_file, snapshot_name, data)

    def post_write(self, data: "SerializableData", index: int = 0) -> None:
        pass

    def get_snapshot_name(self, index: int = 0) -> str:
        index_suffix = f".{index}" if index > 0 else ""
        methodname = self._test_location.testname

        if self._test_location.classname is not None:
            return f"{self._test_location.classname}.{methodname}{index_suffix}"
        return f"{methodname}{index_suffix}"

    def get_filepath(self, index: int) -> str:
        """Returns full filepath where snapshot data is stored."""
        basename = self.get_file_basename(index=index)
        return os.path.join(self.dirname, f"{basename}.{self.file_extension}")

    def get_file_basename(self, index: int) -> str:
        """Returns file basename without extension. Used to create full filepath."""
        return f"{os.path.splitext(os.path.basename(self._test_location.filename))[0]}"

    def __ensure_snapshot_dir(self, index: int) -> None:
        """
        Ensures the folder path for the snapshot file exists.
        """
        try:
            os.makedirs(os.path.dirname(self.get_filepath(index)))
        except FileExistsError:
            pass

    @abstractmethod
    def _read_snapshot_from_file(
        self, snapshot_file: str, snapshot_name: str
    ) -> "SerializableData":
        """
        Read the snapshot file and get only the snapshot data for assertion
        """
        raise NotImplementedError

    @abstractmethod
    def _write_snapshot_to_file(
        self, snapshot_file: str, snapshot_name: str, data: "SerializableData"
    ) -> None:
        """
        Adds the snapshot data to the snapshots read from the file
        """
        raise NotImplementedError
