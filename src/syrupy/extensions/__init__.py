from .amber import AmberSnapshotExtension


DEFAULT_EXTENSION = (
    f"{AmberSnapshotExtension.__module__}.{AmberSnapshotExtension.__name__}"
)
