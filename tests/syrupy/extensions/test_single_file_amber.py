from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.extensions.single_file import (
    SingleFileSnapshotExtension,
    WriteMode,
)


class SingleTextFileExtension(SingleFileSnapshotExtension):
    _write_mode = WriteMode.TEXT


def test_single_file_amber(snapshot):
    storage = SingleTextFileExtension()
    serializer = AmberSnapshotExtension()
    assert {"fruit": "apple"} == snapshot(storage=storage, serializer=serializer)
    assert {"fruit": "orange"} == snapshot(storage=storage, serializer=serializer)
