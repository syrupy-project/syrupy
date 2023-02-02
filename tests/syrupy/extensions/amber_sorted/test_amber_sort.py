import pytest

from syrupy.extensions.amber import (
    AmberDataSerializerSorted,
    AmberSnapshotExtension,
)


class AmberSortedSnapshotExtension(AmberSnapshotExtension):
    serializer_class = AmberDataSerializerSorted


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(AmberSortedSnapshotExtension)


def test_many_sorted(snapshot):
    for i in range(25):
        assert i == snapshot
