from syrupy.types import SerializedData


class SnapshotDoesNotExist(Exception):
    """Snapshot does not exist"""


class FailedToLoadModuleMember(Exception):
    """Failed to load specific member in a module"""


class TaintedSnapshotError(Exception):
    """The snapshot needs to be regenerated."""

    snapshot_data: SerializedData | None

    def __init__(self, snapshot_data: SerializedData | None = None) -> None:
        super().__init__()
        self.snapshot_data = snapshot_data
