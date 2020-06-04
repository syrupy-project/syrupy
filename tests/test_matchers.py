import datetime
import uuid

import pytest

from syrupy.matchers import path_type


def test_matches_expected_type(snapshot):
    my_matcher = path_type(
        {"*": (uuid.UUID,), "date_created": (datetime.datetime,), "nested.id": (int,)}
    )
    actual = {
        "date_created": datetime.datetime.now(),
        "nested": {"id": 4},
        "some_uuid": uuid.uuid4(),
    }
    assert actual == snapshot(matcher=my_matcher)


def test_raises_unexpected_type(snapshot):
    mapping = {
        "*": (uuid.UUID, int),
        "date_created": (datetime.datetime,),
        "date_updated": (datetime.datetime,),
        "nested.id": (str,),
    }
    actual = {
        "date_created": datetime.datetime.now(),
        "date_updated": datetime.date(2020, 6, 1),
        "nested": {"id": 4},
        "some_uuid": uuid.uuid4(),
    }
    with pytest.raises(ValueError):
        assert actual == snapshot(matcher=path_type(mapping))
    assert actual == snapshot(matcher=path_type(mapping, strict=False))
