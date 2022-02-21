from dataclasses import (
    dataclass,
    field,
)
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterator,
    List,
    Optional,
)

from .constants import (
    SNAPSHOT_EMPTY_FOSSIL_KEY,
    SNAPSHOT_UNKNOWN_FOSSIL_KEY,
)

if TYPE_CHECKING:
    from .types import SerializedData


@dataclass(frozen=True)
class Snapshot:
    name: str
    data: Optional["SerializedData"] = None


@dataclass(frozen=True)
class SnapshotEmpty(Snapshot):
    name: str = SNAPSHOT_EMPTY_FOSSIL_KEY


@dataclass(frozen=True)
class SnapshotUnknown(Snapshot):
    name: str = SNAPSHOT_UNKNOWN_FOSSIL_KEY


@dataclass
class SnapshotFossil:
    """A collection of snapshots at a save location"""

    location: str
    _snapshots: Dict[str, "Snapshot"] = field(default_factory=dict)

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


@dataclass
class SnapshotEmptyFossil(SnapshotFossil):
    """This is a saved fossil that is known to be empty and thus can be removed"""

    _snapshots: Dict[str, "Snapshot"] = field(
        default_factory=lambda: {SnapshotEmpty().name: SnapshotEmpty()}
    )

    @property
    def has_snapshots(self) -> bool:
        return False


@dataclass
class SnapshotUnknownFossil(SnapshotFossil):
    """This is a saved fossil that is unclaimed by any extension currently in use"""

    _snapshots: Dict[str, "Snapshot"] = field(
        default_factory=lambda: {SnapshotUnknown().name: SnapshotUnknown()}
    )


@dataclass
class SnapshotFossils:
    _snapshot_fossils: Dict[str, "SnapshotFossil"] = field(default_factory=dict)

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


@dataclass
class DiffedLine:
    a: Optional[str] = None
    b: Optional[str] = None
    c: List[str] = field(default_factory=list)
    diff_a: str = ""
    diff_b: str = ""

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
