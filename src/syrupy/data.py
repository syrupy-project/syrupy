from typing import (
    TYPE_CHECKING,
    Iterator,
    Optional,
    Set,
)

import attr

from .constants import (
    SNAPSHOT_EMPTY_FILE_KEY,
    SNAPSHOT_UNKNOWN_FILE_KEY,
)


if TYPE_CHECKING:
    from .types import SerializedData  # noqa: F401


@attr.s(frozen=True)
class Snapshot(object):
    name: str = attr.ib()
    data: Optional["SerializedData"] = attr.ib(default=None)


@attr.s(frozen=True)
class SnapshotEmpty(Snapshot):
    name: str = attr.ib(default=SNAPSHOT_EMPTY_FILE_KEY, init=False)


@attr.s(frozen=True)
class SnapshotUnknown(Snapshot):
    name: str = attr.ib(default=SNAPSHOT_UNKNOWN_FILE_KEY, init=False)


@attr.s(eq=False)
class SnapshotFile(object):
    filepath: str = attr.ib()
    _snapshots: Set["Snapshot"] = attr.ib(factory=set)

    @property
    def has_snapshots(self) -> bool:
        return bool(self._snapshots)

    def get(self, snapshot_name: str) -> Optional["Snapshot"]:
        for snapshot in self._snapshots:
            if snapshot.name == snapshot_name:
                return snapshot
        return None

    def add(self, snapshot: "Snapshot") -> None:
        self._snapshots.add(snapshot)

    def update(self, snapshot: "Snapshot") -> None:
        self.remove(snapshot.name)
        self.add(snapshot)

    def merge(self, snapshot_file: "SnapshotFile") -> None:
        for snapshot in snapshot_file:
            self.update(snapshot)

    def remove(self, snapshot_name: str) -> None:
        snapshot_to_remove = self.get(snapshot_name)
        if snapshot_to_remove:
            self._snapshots.remove(snapshot_to_remove)

    def __len__(self) -> int:
        return len(self._snapshots)

    def __iter__(self) -> Iterator["Snapshot"]:
        return iter(self._snapshots)


@attr.s(frozen=True)
class SnapshotEmptyFile(SnapshotFile):
    _snapshots: Set["Snapshot"] = attr.ib(
        default=frozenset({SnapshotEmpty()}), init=False,
    )

    @property
    def has_snapshots(self) -> bool:
        return False


@attr.s(frozen=True)
class SnapshotUnknownFile(SnapshotFile):
    _snapshots: Set["Snapshot"] = attr.ib(
        default=frozenset({SnapshotUnknown()}), init=False,
    )


@attr.s
class SnapshotFiles(object):
    _snapshot_files: Set["SnapshotFile"] = attr.ib(factory=set)

    def get(self, filepath: str) -> Optional["SnapshotFile"]:
        for snapshot_file in self._snapshot_files:
            if snapshot_file.filepath == filepath:
                return snapshot_file
        return None

    def add(self, snapshot_file: "SnapshotFile") -> None:
        self._snapshot_files.add(snapshot_file)

    def update(self, snapshot_file: "SnapshotFile") -> None:
        snapshot_file_to_update = self.get(snapshot_file.filepath)
        if snapshot_file_to_update is None:
            snapshot_file_to_update = SnapshotFile(filepath=snapshot_file.filepath)
            self.add(snapshot_file_to_update)
        snapshot_file_to_update.merge(snapshot_file)

    def merge(self, snapshot_files: "SnapshotFiles") -> None:
        for snapshot_file in snapshot_files:
            self.update(snapshot_file)

    def __iter__(self) -> Iterator["SnapshotFile"]:
        return iter(self._snapshot_files)

    def __contains__(self, key: str) -> bool:
        return key in (snapshot_file.filepath for snapshot_file in self._snapshot_files)
