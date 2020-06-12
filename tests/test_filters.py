import datetime

import pytest

from syrupy.filters import paths


def test_filters_path_noop(snapshot):
    with pytest.raises(TypeError, match="required positional argument"):
        paths()


def test_filters_expected_path(snapshot):
    actual = {
        0: "some value",
        "date": datetime.datetime.now(),
        "nested": {"id": 4, "other": "value"},
        "list": [1, 2],
    }
    assert actual == snapshot(exclude=paths("0", "date", "nested.id", "list.0"))


def test_filters_error_prop(snapshot):
    class CustomClass:
        @property
        def include_me(self):
            return "prop value"

        @property
        def exclude_me(self):
            raise Exception("Why you no exclude me?")

    class WithNested(CustomClass):
        nested = CustomClass()

    assert WithNested() == snapshot(exclude=paths("exclude_me", "nested.exclude_me"))
