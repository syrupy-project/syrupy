import datetime
import uuid

import pytest

from syrupy.matchers import (
    PathTypeError,
    path_type,
)


def test_matcher_path_type_noop(snapshot):
    with pytest.raises(PathTypeError, match="argument cannot be empty"):
        path_type()


def test_matches_expected_type(snapshot):
    my_matcher = path_type(
        {"date_created": (datetime.datetime,), "nested.id": (int,)}, types=(uuid.UUID,)
    )
    actual = {
        "date_created": datetime.datetime.now(),
        "nested": {"id": 4},
        "some_uuid": uuid.uuid4(),
    }
    assert actual == snapshot(matcher=my_matcher)


def test_raises_unexpected_type(snapshot):
    kwargs = {
        "mapping": {
            "date_created": (datetime.datetime,),
            "date_updated": (datetime.datetime,),
            "nested.id": (str,),
        },
        "types": (uuid.UUID, int),
    }
    actual = {
        "date_created": datetime.datetime.now(),
        "date_updated": datetime.date(2020, 6, 1),
        "nested": {"id": 4},
        "some_uuid": uuid.uuid4(),
    }
    assert actual == snapshot(matcher=path_type(**kwargs, strict=False))
    with pytest.raises(PathTypeError, match="does not match any of the expected"):
        assert actual == snapshot(matcher=path_type(**kwargs))
