from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from syrupy.data import (
    Snapshot,
    SnapshotFossil,
)
from syrupy.extensions.single_file import SingleFileSnapshotExtension


if TYPE_CHECKING:
    from syrupy.assertion import SnapshotAssertion


@pytest.fixture
def snapshot_single(snapshot):
    return snapshot.use_extension(SingleFileSnapshotExtension)


def test_does_not_write_non_binary(testdir, snapshot_single: "SnapshotAssertion"):
    snapshot_fossil = SnapshotFossil(
        location=str(Path(testdir.tmpdir).joinpath("snapshot_fossil.raw")),
    )
    snapshot_fossil.add(Snapshot(name="snapshot_name", data="non binary data"))
    with pytest.raises(TypeError, match="Expected 'bytes', got 'str'"):
        snapshot_single.extension._write_snapshot_fossil(
            snapshot_fossil=snapshot_fossil
        )
    assert not Path(snapshot_fossil.location).exists()


class TestClass:
    def test_class_method_name(self, snapshot_single):
        assert snapshot_single == b"this is in a test class"

    @pytest.mark.parametrize("content", [b"x", b"y", b"z"])
    def test_class_method_parametrized(self, snapshot_single, content):
        assert snapshot_single == content
