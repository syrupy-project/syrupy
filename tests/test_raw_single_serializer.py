import os
from typing import TYPE_CHECKING

import pytest

from syrupy.data import (
    Snapshot,
    SnapshotFile,
)
from syrupy.serializers.raw_single import RawSingleSnapshotSerializer


if TYPE_CHECKING:
    from syrupy.assertion import SnapshotAssertion


@pytest.fixture
def snapshot_raw(snapshot):
    return snapshot.with_class(serializer_class=RawSingleSnapshotSerializer)


def test_does_not_write_non_binary(testdir, snapshot_raw: "SnapshotAssertion"):
    snapshot_file = SnapshotFile(
        filepath=os.path.join(testdir.tmpdir, "snapshot_file.raw"),
    )
    snapshot_file.add(Snapshot(name="snapshot_name", data="non binary data"))
    with pytest.raises(TypeError, match="Expected 'bytes', got 'str'"):
        snapshot_raw.serializer._write_snapshot_to_file(snapshot_file)
    assert not os.path.exists(snapshot_file.filepath)
