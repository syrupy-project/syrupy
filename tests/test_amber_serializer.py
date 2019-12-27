from collections import namedtuple

import pytest

from syrupy.serializers.amber import AmberSnapshotSerializer


@pytest.fixture
def snapshot(snapshot):
    return snapshot.with_class(serializer_class=AmberSnapshotSerializer)


def test_non_snapshots(snapshot):
    with pytest.raises(AssertionError):
        assert "Lorem ipsum." == "Muspi merol."


def test_empty_snapshot(snapshot):
    assert snapshot == None  # noqa: E711
    assert snapshot == ""


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
    ],
    ids=lambda x: "",
)
def test_string(snapshot, actual):
    assert snapshot == actual


def test_multiple_snapshots(snapshot):
    assert "First." == snapshot
    snapshot.assert_match("Second.")
    snapshot("Third.")


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


def test_tuple(snapshot):
    assert snapshot == ("this", "is", ("a", "tuple"))
    assert snapshot == ExampleTuple(a="this", b="is", c="a", d={"named", "tuple"})


def test_numbers(snapshot):
    assert snapshot == 3.5
    assert snapshot == 7
    assert snapshot == 2 / 6


def test_list(snapshot):
    assert snapshot == [1, 2, "string", {"key": "value"}]


class TestClass:
    def test_name(self, snapshot):
        assert snapshot == "this is in a test class"
