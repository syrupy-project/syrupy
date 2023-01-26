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
    # A tainted snapshot needs to be regenerated
    tainted: Optional[bool] = field(default=None)


@dataclass(frozen=True)
class SnapshotEmpty(Snapshot):
    name: str = SNAPSHOT_EMPTY_FOSSIL_KEY


@dataclass(frozen=True)
class SnapshotUnknown(Snapshot):
    name: str = SNAPSHOT_UNKNOWN_FOSSIL_KEY


@dataclass
class SnapshotCollection:
    """A collection of snapshots at a save location"""

    location: str
    _snapshots: Dict[str, "Snapshot"] = field(default_factory=dict)

    # A tainted collection needs to be regenerated
    tainted: Optional[bool] = field(default=None)

    @property
    def has_snapshots(self) -> bool:
        return bool(self._snapshots)

    def get(self, snapshot_name: str) -> Optional["Snapshot"]:
        return self._snapshots.get(snapshot_name)

    def add(self, snapshot: "Snapshot") -> None:
        self._snapshots[snapshot.name] = snapshot
        if snapshot.name != SNAPSHOT_EMPTY_FOSSIL_KEY:
            self.remove(SNAPSHOT_EMPTY_FOSSIL_KEY)

    def merge(self, snapshot_collection: "SnapshotCollection") -> None:
        for snapshot in snapshot_collection:
            self.add(snapshot)

    def remove(self, snapshot_name: str) -> None:
        self._snapshots.pop(snapshot_name, None)

    def __len__(self) -> int:
        return len(self._snapshots)

    def __iter__(self) -> Iterator["Snapshot"]:
        return iter(self._snapshots.values())


@dataclass
class SnapshotEmptyCollection(SnapshotCollection):
    """This is a saved collection that is known to be empty and thus can be removed"""

    _snapshots: Dict[str, "Snapshot"] = field(
        default_factory=lambda: {SnapshotEmpty().name: SnapshotEmpty()}
    )

    @property
    def has_snapshots(self) -> bool:
        return False


@dataclass
class SnapshotUnknownCollection(SnapshotCollection):
    """This is a saved collection that is unclaimed by any extension currently in use"""

    _snapshots: Dict[str, "Snapshot"] = field(
        default_factory=lambda: {SnapshotUnknown().name: SnapshotUnknown()}
    )


@dataclass
class SnapshotCollections:
    _snapshot_collections: Dict[str, "SnapshotCollection"] = field(default_factory=dict)

    def get(self, location: str) -> Optional["SnapshotCollection"]:
        return self._snapshot_collections.get(location)

    def add(self, snapshot_collection: "SnapshotCollection") -> None:
        self._snapshot_collections[snapshot_collection.location] = snapshot_collection

    def update(self, snapshot_collection: "SnapshotCollection") -> None:
        snapshot_collection_to_update = self.get(snapshot_collection.location)
        if snapshot_collection_to_update is None:
            snapshot_collection_to_update = SnapshotCollection(
                location=snapshot_collection.location
            )
            self.add(snapshot_collection_to_update)
        snapshot_collection_to_update.merge(snapshot_collection)

    def merge(self, snapshot_collections: "SnapshotCollections") -> None:
        for snapshot_collection in snapshot_collections:
            self.update(snapshot_collection)

    def __iter__(self) -> Iterator["SnapshotCollection"]:
        return iter(self._snapshot_collections.values())

    def __contains__(self, key: str) -> bool:
        return key in self._snapshot_collections


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
