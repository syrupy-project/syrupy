class SnapshotDoesNotExist(Exception):
    """Snapshot does not exist"""


class FailedToLoadModuleMember(Exception):
    """Failed to load specific member in a module"""


class FailedToLoadDefaultSnapshotExtension(Exception):
    """Failed to load the default snapshot extension class"""
