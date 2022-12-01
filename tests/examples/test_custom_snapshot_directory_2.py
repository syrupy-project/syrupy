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

from syrupy.extensions.json import JSONSnapshotExtension
from syrupy.location import PyTestLocation


def create_versioned_fixture(version: int):
    class VersionedJSONExtension(JSONSnapshotExtension):
        @classmethod
        def dirname(cls, *, test_location: "PyTestLocation") -> str:
            return str(
                Path(test_location.filepath).parent.joinpath(
                    "__snapshots__", f"v{version}"
                )
            )

    return VersionedJSONExtension


VersionedJSONExtension1 = create_versioned_fixture(version=1)
VersionedJSONExtension2 = create_versioned_fixture(version=2)


@pytest.fixture
def snapshot_v1(snapshot):
    return snapshot.use_extension(VersionedJSONExtension1)


@pytest.fixture
def snapshot_v2(snapshot):
    return snapshot.use_extension(VersionedJSONExtension2)


def test_case_v1(snapshot_v1):
    assert "From v1 of an API" == snapshot_v1


def test_case_v2(snapshot_v2):
    assert "From v2 of an API" == snapshot_v2
