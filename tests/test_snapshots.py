"""
Test snapshot assertions
"""

from collections import namedtuple

import pytest


def test_simple_string(snapshot):
    """Test simple string assertion"""
    assert snapshot == "Loreeeeeem ipsum."


def test_raw_string(snapshot):
    """Test raw string assertion"""
    assert snapshot == r"Raw string"


def test_unicode_string(snapshot):
    """Test unicode string assertion"""
    assert snapshot == "🥞🐍🍯"


def test_multiple_snapshots(snapshot):
    """Test multiple assertions in single test"""
    assert snapshot == "First."
    snapshot.assert_match("Second.")
    assert snapshot == "Third."


@pytest.mark.parametrize("expected", [r"Escaped \n", r"Backslash \u U"])
def test_parametrized_with_special_char(snapshot, expected):
    """Test parametrized support with complex strings"""
    assert expected == snapshot


@pytest.mark.parametrize(
    "actual",
    [
        {"b": True, "c": "Some text.", "d": ["1", 2], "a": {"e": False}},
        {"b": True, "c": "Some ttext.", "d": ["1", 2], "a": {"e": False}},
    ],
)
def test_dict(snapshot, actual):
    """Test dictionary snapshot assertion"""
    assert actual == snapshot


def test_set(snapshot):
    """Test set snapshot assertion"""
    assert snapshot == {"this", "is", "a", "set"}
    assert snapshot == {"this", "is", "a", frozenset({"nested, set"})}


ExampleTuple = namedtuple("ExampleTuple", ["a", "b", "c", "d"])


def test_tuples(snapshot):
    """Test tuple snapshot assertion"""
    assert snapshot == ("this", "is", ("a", "tuple"))
    assert snapshot == ExampleTuple(a="this", b="is", c="a", d={"named", "tuple"})
