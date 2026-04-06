import os
from tempfile import TemporaryDirectory

from hypothesis import example, given, settings
from hypothesis import strategies as st

from syrupy.data import Snapshot, SnapshotCollection
from syrupy.extensions.amber.serializer import (
    AmberDataSerializer,
)


@example("\r\x85")
@given(data=st.text())
@settings(max_examples=1000)
def test_serialize_write_read_round_trip(data):
    """Serialized data survives a write_file/read_file round-trip."""
    serialized = AmberDataSerializer.serialize(data)
    with TemporaryDirectory() as d:
        filepath = os.path.join(d, "test.ambr")
        collection = SnapshotCollection(location=filepath)
        collection.add(Snapshot(name="test", data=serialized))
        AmberDataSerializer.write_file(collection)

        result = AmberDataSerializer.read_file(filepath)
        snapshot = result.get("test")
        assert snapshot is not None
        assert snapshot.data == serialized
