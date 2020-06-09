import datetime
import uuid

import pytest

from syrupy.filters import paths


def test_filters_path_noop(snapshot):
    with pytest.raises(TypeError, match="required positional argument"):
        paths()


def test_filters_expected_path(snapshot):
    actual = {
        "date_created": datetime.datetime.now(),
        "nested": {"id": 4, "other": "value"},
        "some_uuid": uuid.uuid4(),
    }
    assert actual == snapshot(exclude=paths("date_created", "nested.id", "some_uuid"))
