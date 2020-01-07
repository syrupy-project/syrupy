from collections import namedtuple

import pytest


def test_non_snapshots(snapshot):
    with pytest.raises(AssertionError):
        assert "Lorem ipsum." == "Muspi merol."


def test_reflection(snapshot):
    assert snapshot == snapshot


def test_empty_snapshot(snapshot):
    assert snapshot == None  # noqa: E711
    assert snapshot == ""


@pytest.mark.parametrize("actual", [False, True])
def test_bool(actual, snapshot):
    assert actual == snapshot


@pytest.mark.parametrize(
    "actual",
    [
        "",
        r"Raw string",
        r"Escaped \n",
        r"Backslash \u U",
        "🥞🐍🍯",
        "singleline:",
        "- singleline",
        "multi-line\nline 2\nline 3",
        "multi-line\nline 2\n  line 3",
        "string with 'quotes'",
        b"Byte string",
    ],
    ids=lambda x: "",
)
def test_string(snapshot, actual):
    assert snapshot == actual


def test_multiple_snapshots(snapshot):
    assert "First." == snapshot
    snapshot.assert_match("Second.")
    assert snapshot == "Third."


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
    assert snapshot == {"contains", "frozen", frozenset({"1", "2"})}


ExampleTuple = namedtuple("ExampleTuple", ["a", "b", "c", "d"])


def test_tuple(snapshot):
    assert snapshot == ("this", "is", ("a", "tuple"))
    assert snapshot == ExampleTuple(a="this", b="is", c="a", d={"named", "tuple"})


def test_numbers(snapshot):
    assert snapshot == 3.5
    assert snapshot == 7
    assert snapshot == 2 / 6


def test_list(snapshot):
    assert snapshot == [1, 2, "string", {"key": "value"}]


list_cycle = [1, 2, 3]
list_cycle.append(list_cycle)

dict_cycle = {"a": 1, "b": 2, "c": 3}
dict_cycle.update(d=dict_cycle)


@pytest.mark.parametrize("cyclic", [list_cycle, dict_cycle])
def test_cycle(cyclic, snapshot):
    assert cyclic == snapshot


class TestClass:
    def test_class_method_name(self, snapshot):
        assert snapshot == "this is in a test class"

    @pytest.mark.parametrize("actual", ["a", "b", "c"])
    def test_class_method_parametrized(self, snapshot, actual):
        assert snapshot == actual
