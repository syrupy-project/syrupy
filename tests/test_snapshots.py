from collections import namedtuple

import pytest


@pytest.fixture
def snapshot_atomic_write(snapshot):
    update_snapshots = snapshot._update_snapshots
    snapshot._update_snapshots = True
    previous_count = snapshot.num_executions
    yield snapshot
    for i in range(previous_count + 1, snapshot.num_executions):
        snapshot.serializer.write(None, i)
    snapshot._update_snapshots = update_snapshots


def test_simple_string(snapshot):
    assert "Loreeeeeem ipsum." == snapshot


def test_raw_string(snapshot):
    assert r"Raw string" == snapshot


def test_unicode_string(snapshot):
    assert "🥞🐍🍯" == snapshot


def test_multiple_snapshots(snapshot):
    assert "First." == snapshot
    snapshot.assert_match("Second.")
    assert "Third." == snapshot


def test_missing_snapshots(snapshot):
    with pytest.raises(AssertionError, match="Snapshot does not exist"):
        assert "This snapshot should not be written" == snapshot


def test_written_snapshots(snapshot_atomic_write):
    snapshot_data = "This snapshot should not be committed"
    assert snapshot_data == snapshot_atomic_write
    snapshot_file = snapshot_atomic_write.serializer.get_filepath(
        snapshot_atomic_write.num_executions
    )
    with open(snapshot_file, "r") as f:
        assert snapshot_data in f.read()


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
    assert snapshot == {"this", "is", "a", frozenset({"nested, set"})}


ExampleTuple = namedtuple("ExampleTuple", ["a", "b", "c", "d"])


def test_tuples(snapshot):
    assert snapshot == ("this", "is", ("a", "tuple"))
    assert snapshot == ExampleTuple(a="this", b="is", c="a", d={"named", "tuple"})
