from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterator,
    Optional,
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


@attr.s
class SnapshotFile(object):
    filepath: str = attr.ib()
    _snapshots: Dict[str, "Snapshot"] = attr.ib(factory=dict)

    @property
    def has_snapshots(self) -> bool:
        return bool(self._snapshots)

    def get(self, snapshot_name: str) -> Optional["Snapshot"]:
        return self._snapshots.get(snapshot_name)

    def add(self, snapshot: "Snapshot") -> None:
        self._snapshots[snapshot.name] = snapshot

    def merge(self, snapshot_file: "SnapshotFile") -> None:
        for snapshot in snapshot_file:
            self.add(snapshot)

    def remove(self, snapshot_name: str) -> None:
        self._snapshots.pop(snapshot_name, None)

    def __len__(self) -> int:
        return len(self._snapshots)

    def __iter__(self) -> Iterator["Snapshot"]:
        return iter(self._snapshots.values())


SNAPSHOTS_EMPTY = MappingProxyType({SnapshotEmpty().name: SnapshotEmpty()})
SNAPSHOTS_UNKNOWN = MappingProxyType({SnapshotUnknown().name: SnapshotUnknown()})


@attr.s(frozen=True)
class SnapshotEmptyFile(SnapshotFile):
    _snapshots: Dict[str, "Snapshot"] = attr.ib(default=SNAPSHOTS_EMPTY, init=False)

    @property
    def has_snapshots(self) -> bool:
        return False


@attr.s(frozen=True)
class SnapshotUnknownFile(SnapshotFile):
    _snapshots: Dict[str, "Snapshot"] = attr.ib(default=SNAPSHOTS_UNKNOWN, init=False)


@attr.s
class SnapshotFiles(object):
    _snapshot_files: Dict[str, "SnapshotFile"] = attr.ib(factory=dict)

    def get(self, filepath: str) -> Optional["SnapshotFile"]:
        return self._snapshot_files.get(filepath)

    def add(self, snapshot_file: "SnapshotFile") -> None:
        self._snapshot_files[snapshot_file.filepath] = snapshot_file

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
        return iter(self._snapshot_files.values())

    def __contains__(self, key: str) -> bool:
        return key in self._snapshot_files
