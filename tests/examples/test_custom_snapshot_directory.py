"""
Example: Custom Snapshot Directory

Here we extend the Amber extension to change the directory
in which snapshots are stored.

We explicitly name our new fixture "snapshot" to override the
default snapshot fixture. If this is placed in your project's
root conftest.py file, it is equivalent to globally overriding
the default snapshot directory.
"""

import os

import pytest

from syrupy.extensions.amber import AmberSnapshotExtension


DIFFERENT_DIRECTORY = "__snaps_example__"


class DifferentDirectoryExtension(AmberSnapshotExtension):
    @property
    def _dirname(self) -> str:
        test_dirname = os.path.dirname(self.test_location.filename)
        return os.path.join(test_dirname, DIFFERENT_DIRECTORY)


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(DifferentDirectoryExtension)


def test_case_1(snapshot):
    assert "Syrupy is amazing!" == snapshot
