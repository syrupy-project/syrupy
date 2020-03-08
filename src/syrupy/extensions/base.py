import warnings
from abc import (
    ABC,
    abstractmethod,
)
from difflib import ndiff
from gettext import gettext
from itertools import zip_longest
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
)

from typing_extensions import final

from syrupy.constants import (
    SNAPSHOT_DIRNAME,
    SYMBOL_CARRIAGE,
    SYMBOL_ELLIPSIS,
    SYMBOL_NEW_LINE,
)
from syrupy.data import (
    DiffedLine,
    Snapshot,
    SnapshotEmptyFossil,
    SnapshotFossil,
    SnapshotFossils,
)
from syrupy.exceptions import SnapshotDoesNotExist
from syrupy.terminal import (
    context_style,
    received_diff_style,
    received_style,
    reset,
    snapshot_diff_style,
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
        return f"{self.test_location.snapshot_name}{index_suffix}"

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
    ) -> Iterator[str]:
        for line in self.__diff_lines(str(snapshot_data), str(serialized_data)):
            yield reset(line)

    @property
    def _ends(self) -> Dict[str, str]:
        return {"\n": self._marker_new_line, "\r": self._marker_carriage}

    @property
    def _context_line_count(self) -> int:
        return 1

    @property
    def _context_line_max(self) -> int:
        return self._context_line_count * 2

    @property
    def _marker_context_max(self) -> str:
        return SYMBOL_ELLIPSIS

    @property
    def _marker_new_line(self) -> str:
        return SYMBOL_NEW_LINE

    @property
    def _marker_carriage(self) -> str:
        return SYMBOL_CARRIAGE

    def __diff_lines(self, a: str, b: str) -> Iterator[str]:
        for line in self.__diffed_lines(a, b):
            show_ends = (
                self.__strip_ends(line.a[1:]) == self.__strip_ends(line.b[1:])
                if line.is_complete
                else False
            )
            if line.has_snapshot:
                yield self.__format_line(
                    line.a, line.diff_a, snapshot_style, snapshot_diff_style, show_ends
                )
            if line.has_received:
                yield self.__format_line(
                    line.b, line.diff_b, received_style, received_diff_style, show_ends
                )
            yield from map(context_style, self.__limit_context(line.c))

    def __diffed_lines(self, a: str, b: str) -> Iterator["DiffedLine"]:
        staged_diffed_line: Optional["DiffedLine"] = None
        for line in ndiff(a.splitlines(keepends=True), b.splitlines(keepends=True)):
            is_context_line = line[0] == " "
            is_snapshot_line = line[0] == "-"
            is_received_line = line[0] == "+"
            is_diff_line = line[0] == "?"

            if is_context_line or is_diff_line:
                line = self.__strip_ends(line)

            if staged_diffed_line:
                if is_diff_line:
                    if staged_diffed_line.has_received:
                        staged_diffed_line.diff_b = line
                    elif staged_diffed_line.has_snapshot:
                        staged_diffed_line.diff_a = line
                    # else: should never happen because then it would have
                    # encounted a diff line without any previously staged line
                else:
                    should_unstage = (
                        staged_diffed_line.is_complete
                        or (staged_diffed_line.has_snapshot and is_snapshot_line)
                        or (staged_diffed_line.has_received and is_received_line)
                        or (staged_diffed_line.is_context and not is_context_line)
                    )
                    if should_unstage:
                        yield staged_diffed_line
                        staged_diffed_line = None
                    elif is_snapshot_line:
                        staged_diffed_line.a = line
                    elif is_received_line:
                        staged_diffed_line.b = line
                    elif is_context_line:
                        staged_diffed_line.c.append(line)

            if not staged_diffed_line:
                if is_snapshot_line:
                    staged_diffed_line = DiffedLine(a=line)
                elif is_received_line:
                    staged_diffed_line = DiffedLine(b=line)
                elif is_context_line:
                    staged_diffed_line = DiffedLine(c=[line])
                # else: should never happen because then it would have
                # encounted a diff line without any previously staged line

        if staged_diffed_line:
            yield staged_diffed_line

    def __format_line(
        self,
        line: str,
        diff_markers: str,
        line_style: Callable[[str], str],
        diff_style: Callable[[str], str],
        show_ends: bool,
    ) -> str:
        if show_ends:
            for old, new in self._ends.items():
                line = line.replace(old, new)
        else:
            line = self.__strip_ends(line)
        return "".join(
            diff_style(char) if str(marker) in "-+^" else line_style(char)
            for marker, char in zip_longest(diff_markers.rstrip(), line)
            if char is not None
        )

    def __limit_context(self, lines: List[str]) -> Iterator[str]:
        yield from lines[: self._context_line_count]
        num_lines = len(lines)
        if num_lines:
            if num_lines > self._context_line_max:
                count_leading_whitespace: Callable[[str], int] = (
                    lambda s: len(s) - len(s.lstrip())  # noqa: E731
                )
                if self._context_line_count:
                    num_space = (
                        count_leading_whitespace(lines[self._context_line_count - 1])
                        + count_leading_whitespace(lines[-self._context_line_count])
                    ) // 2
                else:
                    num_space = count_leading_whitespace(lines[num_lines // 2])
                yield " " * num_space + self._marker_context_max
            if self._context_line_count and num_lines > 1:
                yield from lines[-self._context_line_count :]  # noqa: E203

    def __strip_ends(self, line: str) -> str:
        return line.rstrip("".join(self._ends.keys()))


class AbstractSyrupyExtension(SnapshotSerializer, SnapshotFossilizer, SnapshotReporter):
    def __init__(self, test_location: "TestLocation"):
        self._test_location = test_location

    @property
    def test_location(self) -> "TestLocation":
        return self._test_location
