from collections import namedtuple

import pytest


def test_non_snapshots(snapshot):
    with pytest.raises(AssertionError):
        assert "Lorem ipsum." == "Muspi merol."


def test_simple_string(snapshot):
    assert "Loreeeeeem ipsum." == snapshot


def test_raw_string(snapshot):
    assert r"Raw string" == snapshot


def test_unicode_string(snapshot):
    assert "🥞🐍🍯" == snapshot


def test_multiple_snapshots(snapshot):
    assert "First." == snapshot
    snapshot.assert_match("Second.")
    snapshot("Third.")


@pytest.mark.parametrize("expected", [r"Escaped \n", r"Backslash \u U"])
def test_parametrized_with_special_char(snapshot, expected):
    assert expected == snapshot


@pytest.mark.parametrize(
    "actual",
    [
        {"b": True, "c": "Some text.", "d": ["1", 2], "a": {"e": False}},
        {"b": True, "c": "Some ttext.", "d": ["1", 2], "a": {"e": False}},
    ],
)
def test_dict(snapshot, actual):
    assert actual == snapshot


def test_set(snapshot):
    assert snapshot == {"this", "is", "a", "set"}


ExampleTuple = namedtuple("ExampleTuple", ["a", "b", "c", "d"])


def test_tuples(snapshot):
    assert snapshot == ("this", "is", ("a", "tuple"))
    assert snapshot == ExampleTuple(a="this", b="is", c="a", d={"named", "tuple"})


class TestClass:
    def test_name(self, snapshot):
        assert snapshot == "this is in a test class"
