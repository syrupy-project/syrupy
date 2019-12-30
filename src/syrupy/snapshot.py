from typing import (
    TYPE_CHECKING,
    Dict,
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
    from .types import SerializableData


@attr.s
class SnapshotData(object):
    data: "SerializableData" = attr.ib(default=None)


@attr.s
class SnapshotFile(object):
    filepath: str = attr.ib()
    snapshots: Dict[str, "SnapshotData"] = attr.ib(default={})


@attr.s
class SnapshotEmptyFile(SnapshotFile):
    snapshots = {SNAPSHOT_EMPTY_FILE_KEY: SnapshotData()}


@attr.s
class SnapshotUnknownFile(SnapshotFile):
    snapshots = {SNAPSHOT_UNKNOWN_FILE_KEY: SnapshotData()}


@attr.s
class SnapshotFiles(object):
    _snapshot_files: Set["SnapshotFile"] = attr.ib(default=set())

    def get(self, filepath: str) -> Optional["SnapshotFile"]:
        for snapshot_file in self._snapshot_files:
            if snapshot_file.filepath == filepath:
                return snapshot_file
        return None

    def add(self, snapshot_file: "SnapshotFile") -> None:
        self._snapshot_files.add(snapshot_file)

    def merge(self, snapshot_file: "SnapshotFile") -> None:
        snapshot_file_to_update = self.get(snapshot_file.filepath)
        if not snapshot_file_to_update:
            snapshot_file_to_update = SnapshotFile(filepath=snapshot_file.filepath)
            self._snapshot_files.add(snapshot_file_to_update)
        snapshot_file_to_update.snapshots.update(snapshot_file.snapshots)

    def __iter__(self) -> Iterator["SnapshotFile"]:
        return iter(self._snapshot_files)

    def __contains__(self, key: str) -> bool:
        return key in (snapshot_file.filepath for snapshot_file in self._snapshot_files)
