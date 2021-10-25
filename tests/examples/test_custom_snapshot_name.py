"""
Example: Custom Snapshot Name
"""
import pytest

from syrupy.extensions.amber import AmberSnapshotExtension


class CanadianNameExtension(AmberSnapshotExtension):
    def get_snapshot_name(self, *, snapshot_name_suffix: str) -> str:
        original_name = super(CanadianNameExtension, self).get_snapshot_name(
            snapshot_name_suffix=snapshot_name_suffix
        )
        return f"{original_name}🇨🇦"


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(CanadianNameExtension)


def test_canadian_name(snapshot):
    assert "Name should be test_canadian_name🇨🇦." == snapshot
