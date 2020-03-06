import warnings
from abc import (
    ABC,
    abstractmethod,
)
from collections import deque
from difflib import ndiff
from gettext import gettext
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Deque,
    Generator,
    Optional,
    Set,
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
    context_style,
    mute,
    received_style,
    reset,
    snapshot_style,
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
        return str(Path(self._dirname).joinpath(f"{basename}.{self._file_extension}"))

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
        if not self.test_location.matches_snapshot_location(snapshot_location):
            warning_msg = gettext(
                "\nCan not relate snapshot location '{}' to the test location."
                "\nConsider adding '{}' to the generated location."
            ).format(snapshot_location, self.test_location.filename)
            warnings.warn(warning_msg)
        snapshot_name = self.get_snapshot_name(index=index)
        if not self.test_location.matches_snapshot_name(snapshot_name):
            warning_msg = gettext(
                "\nCan not relate snapshot name '{}' to the test location."
                "\nConsider adding '{}' to the generated name."
            ).format(snapshot_name, self.test_location.testname)
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
        test_dir = Path(self.test_location.filepath).parent
        return str(test_dir.joinpath(SNAPSHOT_DIRNAME))

    @property
    @abstractmethod
    def _file_extension(self) -> str:
        raise NotImplementedError

    def _get_file_basename(self, *, index: int) -> str:
        """Returns file basename without extension. Used to create full filepath."""
        return self.test_location.filename

    def __ensure_snapshot_dir(self, *, index: int) -> None:
        """
        Ensures the folder path for the snapshot file exists.
        """
        try:
            Path(self.get_location(index=index)).parent.mkdir(parents=True)
        except FileExistsError:
            pass


class SnapshotReporter(ABC):
    def diff_lines(
        self, serialized_data: "SerializedData", snapshot_data: "SerializedData"
    ) -> Generator[str, None, None]:
        for line in self.__diff_lines(str(snapshot_data), str(serialized_data)):
            yield reset(line)

    @property
    def __max_context_lines(self) -> int:
        return 3

    def __get_context(
        self, queue: Deque[str], before: bool
    ) -> Generator[str, None, None]:
        extra_lines = len(queue) == self.__max_context_lines + 1
        for idx, context_line in enumerate(queue):
            if before and extra_lines and idx == 0:
                yield context_style("...")
            elif not before and extra_lines and idx == len(queue) - 1:
                yield context_style("...")
            else:
                yield context_style(context_line.rstrip("\r\n"))

    def __show_line_endings(self, a: str, b: str) -> bool:
        if a is None or b is None:
            return False
        a_count = {"\r": 0, "\n": 0}
        b_count = {"\r": 0, "\n": 0}
        for c in a:
            if c in a_count:
                a_count[c] += 1
        for c in b:
            if c in b_count:
                b_count[c] += 1
        return a_count != b_count

    def __sanitize_line(
        self, line: Optional[str], show_line_ending: bool
    ) -> Optional[str]:
        if line is None:
            return line
        if show_line_ending:
            line = line.replace("\n", mute("\u2424")).replace("\r", mute("\u240D"))
        line = line.rstrip("\r\n")

        if line.endswith(" "):
            n_spaces = len(line) - len(line.rstrip(" "))
            line = line.rstrip(" ") + mute("\u00B7" * n_spaces)

        return line

    def __diff_lines(self, a: str, b: str) -> Generator[str, None, None]:
        context_queue: Deque[str] = deque([], self.__max_context_lines + 1)
        staged_line = None
        last_match_index = None
        for idx, line in enumerate(
            ndiff(a.splitlines(keepends=True), b.splitlines(keepends=True))
        ):
            marker = line[0]

            if staged_line is not None:
                yield from self.__get_context(context_queue, True)
                show_line_endings = self.__show_line_endings(staged_line, line)
                staged_line = self.__sanitize_line(staged_line, show_line_endings)
                line = self.__sanitize_line(line, show_line_endings)
                yield from self.__diff_line(line, staged_line)
                staged_line = None
                context_queue.clear()
                continue

            if marker == " ":
                context_queue.append(line)

                if (
                    last_match_index is not None
                    and idx - last_match_index == self.__max_context_lines + 1
                ):
                    yield from self.__get_context(context_queue, False)
                continue

            if marker in ("+", "-"):
                last_match_index = idx
                staged_line = line
                continue

    def __diff_line(
        self, inline_marker_ctx: str, line: str
    ) -> Generator[str, None, None]:
        marker = line[0]

        if marker == "-":
            yield snapshot_style(line)

        if marker == "+":
            yield received_style(line)


class AbstractSyrupyExtension(SnapshotSerializer, SnapshotFossilizer, SnapshotReporter):
    def __init__(self, test_location: "TestLocation"):
        self._test_location = test_location

    @property
    def test_location(self) -> "TestLocation":
        return self._test_location
