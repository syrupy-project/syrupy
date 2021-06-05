from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Set,
)

from syrupy.data import SnapshotFossil
from syrupy.extensions.base import AbstractSyrupyExtension

from .serializer import DataSerializer

if TYPE_CHECKING:
    from syrupy.types import SerializableData


class AmberSnapshotExtension(AbstractSyrupyExtension):
    """
    An amber snapshot file stores data in the following format:
    """

    def serialize(self, data: "SerializableData", **kwargs: Any) -> str:
        """
        Returns the serialized form of 'data' to be compared
        with the snapshot data written to disk.
        """
        return DataSerializer.serialize(data, **kwargs)

    def delete_snapshots(
        self, snapshot_location: str, snapshot_names: Set[str]
    ) -> None:
        snapshot_fossil_to_update = DataSerializer.read_file(snapshot_location)
        for snapshot_name in snapshot_names:
            snapshot_fossil_to_update.remove(snapshot_name)

        if snapshot_fossil_to_update.has_snapshots:
            DataSerializer.write_file(snapshot_fossil_to_update)
        else:
            Path(snapshot_location).unlink()

    @property
    def _file_extension(self) -> str:
        return "ambr"

    def _read_snapshot_fossil(self, snapshot_location: str) -> "SnapshotFossil":
        return DataSerializer.read_file(snapshot_location)

    def _read_snapshot_data_from_location(
        self, snapshot_location: str, snapshot_name: str
    ) -> Optional["SerializableData"]:
        snapshot = self._read_snapshot_fossil(snapshot_location).get(snapshot_name)
        return snapshot.data if snapshot else None

    def _write_snapshot_fossil(self, *, snapshot_fossil: "SnapshotFossil") -> None:
        snapshot_fossil_to_update = DataSerializer.read_file(snapshot_fossil.location)
        snapshot_fossil_to_update.merge(snapshot_fossil)
        DataSerializer.write_file(snapshot_fossil_to_update)


__all__ = ["AmberSnapshotExtension", "DataSerializer"]
