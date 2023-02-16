from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from syrupy.data import (
    Snapshot,
    SnapshotCollection,
)
from syrupy.extensions.single_file import (
    SingleFileSnapshotExtension,
    WriteMode,
)

if TYPE_CHECKING:
    from syrupy.assertion import SnapshotAssertion


@pytest.fixture
def snapshot_single(snapshot):
    return snapshot.use_extension(SingleFileSnapshotExtension)


class SingleFileUTF8SnapshotExtension(SingleFileSnapshotExtension):
    _write_mode = WriteMode.TEXT


@pytest.fixture
def snapshot_utf8(snapshot):
    return snapshot.use_extension(SingleFileUTF8SnapshotExtension)


def test_does_not_write_non_binary(testdir, snapshot_single: "SnapshotAssertion"):
    snapshot_collection = SnapshotCollection(
        location=str(Path(testdir.tmpdir).joinpath("snapshot_collection.raw")),
    )
    snapshot_collection.add(Snapshot(name="snapshot_name", data="non binary data"))
    with pytest.raises(TypeError, match="Expected 'bytes', got 'str'"):
        snapshot_single.extension._write_snapshot_collection(
            snapshot_collection=snapshot_collection
        )
    assert not Path(snapshot_collection.location).exists()


class TestClass:
    def test_class_method_name(self, snapshot_single):
        assert snapshot_single == b"this is in a test class"

    @pytest.mark.parametrize("content", [b"x", b"y", b"z"])
    def test_class_method_parametrized(self, snapshot_single, content):
        assert snapshot_single == content


def test_underscore(snapshot_single):
    assert snapshot_single == b"apple"


def test_____underscore(snapshot_single):
    assert snapshot_single == b"orange"


@pytest.mark.parametrize(
    "content", [b"", b"_", b"a?", b"space space", b".123~!@#$%^&*()/[]{}|"]
)
def test_special_characters(snapshot_single, content):
    assert snapshot_single == content


@pytest.mark.parametrize("content", ["greek ῴ"])
def test_unicode(snapshot_utf8, content):
    assert snapshot_utf8 == "apple"


class DotInFileExtension(SingleFileSnapshotExtension):
    _file_extension = "ext2.ext1"


@pytest.fixture
def snapshot_dot_in_file_extension(snapshot):
    return snapshot.use_extension(DotInFileExtension)


def test_dot_in_file_extension(snapshot_dot_in_file_extension):
    assert b"expected_data" == snapshot_dot_in_file_extension
