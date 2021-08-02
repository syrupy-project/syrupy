import datetime
import uuid

import pytest

from syrupy.extensions.amber.serializer import Repr
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
    with pytest.raises(AssertionError, match="does not match any of the expected"):
        assert actual == snapshot(matcher=path_type(**kwargs))


def test_matches_non_deterministic_snapshots(snapshot):
    def matcher(data, path):
        if isinstance(data, uuid.UUID):
            return Repr("UUID(...)")
        if isinstance(data, datetime.datetime):
            return Repr("datetime.datetime(...)")
        if tuple(p for p, _ in path[-2:]) == ("c", 0):
            return "Your wish is my command"
        return data

    assert {
        "a": uuid.uuid4(),
        "b": {"b_1": "This is deterministic", "b_2": datetime.datetime.now()},
        "c": ["Replace this one", "Do not replace this one"],
    } == snapshot(matcher=matcher)
    assert {
        "a": uuid.UUID("06335e84-2872-4914-8c5d-3ed07d2a2f16"),
        "b": {
            "b_1": "This is deterministic",
            "b_2": datetime.datetime(year=2020, month=5, day=31),
        },
        "c": ["Replace this one", "Do not replace this one"],
    } == snapshot


def test_matches_regex_in_regex_mode(snapshot):
    my_matcher = path_type(
        {
            r"data\.list\..*\.date_created": (datetime.datetime,),
            r"any_number": (int,),
        },
        regex=True,
    )
    actual = {
        "data": {
            "list": [
                {"k": "1", "date_created": datetime.datetime.now()},
                {"k": "2", "date_created": datetime.datetime.now()},
            ],
        },
        "any_number": 3,
        "any_number_adjacent": "hi",
        "specific_number": 5,
    }
    assert actual == snapshot(matcher=my_matcher)
