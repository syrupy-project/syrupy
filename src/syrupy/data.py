from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterator,
    List,
    Optional,
)

import attr

from .constants import (
    SNAPSHOT_EMPTY_FOSSIL_KEY,
    SNAPSHOT_UNKNOWN_FOSSIL_KEY,
)


if TYPE_CHECKING:
    from .types import SerializedData  # noqa: F401


@attr.s(frozen=True)
class Snapshot:
    name: str = attr.ib()
    data: Optional["SerializedData"] = attr.ib(default=None)


@attr.s(frozen=True)
class SnapshotEmpty(Snapshot):
    name: str = attr.ib(default=SNAPSHOT_EMPTY_FOSSIL_KEY, init=False)


@attr.s(frozen=True)
class SnapshotUnknown(Snapshot):
    name: str = attr.ib(default=SNAPSHOT_UNKNOWN_FOSSIL_KEY, init=False)


@attr.s
class SnapshotFossil:
    """A collection of snapshots at a save location"""

    location: str = attr.ib()
    _snapshots: Dict[str, "Snapshot"] = attr.ib(factory=dict)

    @property
    def has_snapshots(self) -> bool:
        return bool(self._snapshots)

    def get(self, snapshot_name: str) -> Optional["Snapshot"]:
        return self._snapshots.get(snapshot_name)

    def add(self, snapshot: "Snapshot") -> None:
        self._snapshots[snapshot.name] = snapshot
        if snapshot.name != SNAPSHOT_EMPTY_FOSSIL_KEY:
            self.remove(SNAPSHOT_EMPTY_FOSSIL_KEY)

    def merge(self, snapshot_fossil: "SnapshotFossil") -> None:
        for snapshot in snapshot_fossil:
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
class SnapshotEmptyFossil(SnapshotFossil):
    """This is a saved fossil that is known to be empty and thus can be removed"""

    _snapshots: Dict[str, "Snapshot"] = attr.ib(default=SNAPSHOTS_EMPTY, init=False)

    @property
    def has_snapshots(self) -> bool:
        return False


@attr.s(frozen=True)
class SnapshotUnknownFossil(SnapshotFossil):
    """This is a saved fossil that is unclaimed by any extension currently in use"""

    _snapshots: Dict[str, "Snapshot"] = attr.ib(default=SNAPSHOTS_UNKNOWN, init=False)


@attr.s
class SnapshotFossils:
    _snapshot_fossils: Dict[str, "SnapshotFossil"] = attr.ib(factory=dict)

    def get(self, location: str) -> Optional["SnapshotFossil"]:
        return self._snapshot_fossils.get(location)

    def add(self, snapshot_fossil: "SnapshotFossil") -> None:
        self._snapshot_fossils[snapshot_fossil.location] = snapshot_fossil

    def update(self, snapshot_fossil: "SnapshotFossil") -> None:
        snapshot_fossil_to_update = self.get(snapshot_fossil.location)
        if snapshot_fossil_to_update is None:
            snapshot_fossil_to_update = SnapshotFossil(
                location=snapshot_fossil.location
            )
            self.add(snapshot_fossil_to_update)
        snapshot_fossil_to_update.merge(snapshot_fossil)

    def merge(self, snapshot_fossils: "SnapshotFossils") -> None:
        for snapshot_fossil in snapshot_fossils:
            self.update(snapshot_fossil)

    def __iter__(self) -> Iterator["SnapshotFossil"]:
        return iter(self._snapshot_fossils.values())

    def __contains__(self, key: str) -> bool:
        return key in self._snapshot_fossils


@attr.s
class DiffedLine:
    a: str = attr.ib(default=None)
    b: str = attr.ib(default=None)
    c: List[str] = attr.ib(factory=list)
    diff_a: str = attr.ib(default="")
    diff_b: str = attr.ib(default="")

    @property
    def has_snapshot(self) -> bool:
        return self.a is not None

    @property
    def has_received(self) -> bool:
        return self.b is not None

    @property
    def is_complete(self) -> bool:
        return self.has_snapshot and self.has_received

    @property
    def is_context(self) -> bool:
        return bool(self.c)
