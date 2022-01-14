import datetime

import pytest

from syrupy.extensions.json import JSONSnapshotExtension
from syrupy.filters import (
    paths,
    props,
)


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.use_extension(JSONSnapshotExtension)


@pytest.mark.parametrize(
    "content",
    [
        {},
        ["an array"],
        {
            "str": "foo",
            "int": -1,
            "float": 4.2,
            "array": [1, 2, 3],
            "null": None,
            "datetime": datetime.datetime(2021, 1, 31, 23, 59),
        },
    ],
)
def test_serializer(snapshot_json, content):
    assert snapshot_json == content


def test_exclude_simple(snapshot_json):
    content = {
        "id": 123456789,
        "foo": "__SHOULD_BE_REMOVED_FROM_JSON__",
        "I'm": "still alive",
        "nested": {
            "foo": "is still alive",
        },
    }
    assert snapshot_json(exclude=props("id", "foo")) == content
    assert snapshot_json(exclude=paths("id", "foo")) == content


def test_exclude_nested(snapshot_json):
    content = {
        "a": "b",
        "foo": {
            "bar": "__SHOULD_BE_REMOVED_FROM_JSON__",
        },
        "x": {
            "y": {
                "z": "__SHOULD_BE_REMOVED_FROM_JSON__",
                "zz": "I'm still there",
            }
        },
    }
    assert snapshot_json(exclude=paths("foo.bar", "x.y.z")) == content


def test_exclude_in_json_with_empty_values(snapshot_json):
    content = {
        "foo": "bar",
        "none": None,
        "empty_dict": {},
        "empty_list": [],
    }
    assert snapshot_json(exclude=props("foo")) == content
