"""
Example: Custom Snapshot Directory

Here we extend the Amber extension to change the directory
in which snapshots are stored.

We explicitly name our new fixture "snapshot" to override the
default snapshot fixture. If this is placed in your project's
root conftest.py file, it is equivalent to globally overriding
the default snapshot directory.
"""

from pathlib import Path

import pytest

from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.location import PyTestLocation

DIFFERENT_DIRECTORY = "__snaps_example__"


class DifferentDirectoryExtension(AmberSnapshotExtension):
    @classmethod
    def dirname(cls, *, test_location: "PyTestLocation") -> str:
        return str(Path(test_location.filepath).parent.joinpath(DIFFERENT_DIRECTORY))


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(DifferentDirectoryExtension)


def test_case_1(snapshot):
    assert "Syrupy is amazing!" == snapshot
