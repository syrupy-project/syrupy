"""Example: Custom snapshot defaults

Here we modify snapshot defaults globally, instead of per assert.
This gives the ability to modify the snapshot functionality to your hearts content
and then simply re-use them, without having to pass those defaults to every assert.
Especially useful if there's a lot of tests that need to modify the default behaviour.
"""
import pytest

from syrupy.extensions.json import JSONSnapshotExtension
from syrupy.filters import paths
from syrupy.matchers import path_type


@pytest.fixture
def snapshot_matcher(snapshot):
    return snapshot.with_defaults(matcher=path_type(mapping={"my-field": (str, int)}))


@pytest.fixture
def snapshot_exclude(snapshot_matcher):
    return snapshot_matcher.with_defaults(exclude=paths("excluded"))


@pytest.fixture
def snapshot_json(snapshot_exclude):
    return snapshot_exclude.with_defaults(extension_class=JSONSnapshotExtension)


def test_asserting_multiple_times(snapshot_matcher):
    assert {"my-field": "my-string", "excluded": "value"} == snapshot_matcher
    assert {"my-field": 12345, "excluded": "value"} == snapshot_matcher


def test_asserting_multiple_times_chained(snapshot_exclude):
    assert {"my-field": "my-string", "excluded": "value"} == snapshot_exclude
    assert {"my-field": 12345, "excluded": "value"} == snapshot_exclude


def test_asserting_multiple_times_chained_json(snapshot_json):
    assert {"my-field": "my-string", "excluded": "value"} == snapshot_json
    assert {"my-field": 12345, "excluded": "value"} == snapshot_json
