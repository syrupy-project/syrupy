from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Dict,
    Iterator,
    Optional,
)

import attr

from .constants import (
    SNAPSHOT_EMPTY_CACHE_KEY,
    SNAPSHOT_UNKNOWN_CACHE_KEY,
)


if TYPE_CHECKING:
    from .types import SerializedData  # noqa: F401


@attr.s(frozen=True)
class Snapshot(object):
    name: str = attr.ib()
    data: Optional["SerializedData"] = attr.ib(default=None)


@attr.s(frozen=True)
class SnapshotEmpty(Snapshot):
    name: str = attr.ib(default=SNAPSHOT_EMPTY_CACHE_KEY, init=False)


@attr.s(frozen=True)
class SnapshotUnknown(Snapshot):
    name: str = attr.ib(default=SNAPSHOT_UNKNOWN_CACHE_KEY, init=False)


@attr.s
class SnapshotCache(object):
    location: str = attr.ib()
    _snapshots: Dict[str, "Snapshot"] = attr.ib(factory=dict)

    @property
    def has_snapshots(self) -> bool:
        return bool(self._snapshots)

    def get(self, snapshot_name: str) -> Optional["Snapshot"]:
        return self._snapshots.get(snapshot_name)

    def add(self, snapshot: "Snapshot") -> None:
        self._snapshots[snapshot.name] = snapshot

    def merge(self, snapshot_cache: "SnapshotCache") -> None:
        for snapshot in snapshot_cache:
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
class SnapshotEmptyCache(SnapshotCache):
    """This is a cache that is known to be empty and thus can be removed"""

    _snapshots: Dict[str, "Snapshot"] = attr.ib(default=SNAPSHOTS_EMPTY, init=False)

    @property
    def has_snapshots(self) -> bool:
        return False


@attr.s(frozen=True)
class SnapshotUnknownCache(SnapshotCache):
    """
    This is a cache that exists but no snapshot extension currently
    in use has claimed
    """

    _snapshots: Dict[str, "Snapshot"] = attr.ib(default=SNAPSHOTS_UNKNOWN, init=False)


@attr.s
class SnapshotCaches(object):
    _snapshot_caches: Dict[str, "SnapshotCache"] = attr.ib(factory=dict)

    def get(self, location: str) -> Optional["SnapshotCache"]:
        return self._snapshot_caches.get(location)

    def add(self, snapshot_cache: "SnapshotCache") -> None:
        self._snapshot_caches[snapshot_cache.location] = snapshot_cache

    def update(self, snapshot_cache: "SnapshotCache") -> None:
        snapshot_cache_to_update = self.get(snapshot_cache.location)
        if snapshot_cache_to_update is None:
            snapshot_cache_to_update = SnapshotCache(location=snapshot_cache.location)
            self.add(snapshot_cache_to_update)
        snapshot_cache_to_update.merge(snapshot_cache)

    def merge(self, snapshot_caches: "SnapshotCaches") -> None:
        for snapshot_cache in snapshot_caches:
            self.update(snapshot_cache)

    def __iter__(self) -> Iterator["SnapshotCache"]:
        return iter(self._snapshot_caches.values())

    def __contains__(self, key: str) -> bool:
        return key in self._snapshot_caches
