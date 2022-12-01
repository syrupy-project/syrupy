"""
Example: Custom Snapshot Name
"""
import pytest

from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.location import PyTestLocation
from syrupy.types import SnapshotIndex


class CanadianNameExtension(AmberSnapshotExtension):
    @classmethod
    def get_snapshot_name(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex"
    ) -> str:
        original_name = AmberSnapshotExtension.get_snapshot_name(
            test_location=test_location, index=index
        )
        return f"{original_name}🇨🇦"


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(CanadianNameExtension)


def test_canadian_name(snapshot):
    assert "Name should be test_canadian_name🇨🇦." == snapshot
