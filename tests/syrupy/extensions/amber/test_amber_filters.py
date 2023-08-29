import datetime

import pytest

from syrupy.filters import (
    paths,
    paths_include,
    props,
)


def test_filters_path_noop():
    with pytest.raises(TypeError, match="At least 1 path argument is required."):
        paths()


def test_filters_expected_paths(snapshot):
    actual = {
        0: "some value",
        "date": datetime.datetime.now(),
        "nested": {"id": 4, "other": "value"},
        "list": [1, 2],
    }
    assert actual == snapshot(exclude=paths("0", "date", "nested.id", "list.0"))


def test_filters_prop_noop():
    with pytest.raises(TypeError, match="At least 1 prop name is required."):
        props()


def test_filters_expected_props(snapshot):
    actual = {
        0: "some value",
        "date": datetime.datetime.now(),
        "nested": {"id": 4, "other": "value"},
        "list": [1, 2],
    }
    assert actual == snapshot(exclude=props("0", "date", "id"))


def test_only_includes_expected_props(snapshot):
    actual = {
        0: "some value",
        "date": "utc",
        "nested": {"id": 4, "other": "value"},
        "list": [1, 2],
    }
    # Note that "id" won't get included because "nested" (its parent) is not included.
    assert actual == snapshot(include=props("0", "date", "id"))
    assert actual == snapshot(include=paths("0", "date", "nested", "nested.id"))


def test_includes_nested_path(snapshot):
    actual = {
        "ignore-me": True,
        "include-me": False,
        "layer1": {"layer2": [0, True]},
    }
    assert actual == snapshot(
        include=paths_include(["include-me"], ["layer1", "layer2", "1"])
    )


@pytest.mark.parametrize(
    "predicate", [paths("exclude_me", "nested.exclude_me"), props("exclude_me")]
)
def test_filters_error_prop(snapshot, predicate):
    class CustomClass:
        @property
        def include_me(self):
            return "prop value"

        @property
        def exclude_me(self):
            raise Exception("Why you no exclude me?")

    class WithNested(CustomClass):
        nested = CustomClass()

    assert WithNested() == snapshot(exclude=predicate)
