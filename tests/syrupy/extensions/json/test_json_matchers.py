import datetime
import random

import pytest

from syrupy.extensions.json import JSONSnapshotExtension
from syrupy.matchers import path_type


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.use_extension(JSONSnapshotExtension)


def test_matcher(snapshot_json):
    content = {
        "int": random.randint(1, 100),
        "date": datetime.datetime.utcnow(),
        "foo": {
            "x": "y",
            "another_date": datetime.datetime.utcnow(),
        },
    }
    matcher = path_type(
        {
            "int": (int,),
            "date": (datetime.date,),
            "foo.another_date": (dict, datetime.datetime),
        }
    )
    assert snapshot_json(matcher=matcher) == content
