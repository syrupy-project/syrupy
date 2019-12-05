import pytest


def test_simple_string(snapshot):
    assert "Loreeeeeem ipsum." == snapshot


def test_raw_string(snapshot):
    assert r"Raw string" == snapshot


def test_multiple_snapshots(snapshot):
    assert "First." == snapshot
    snapshot.assert_match("Second.")
    assert "Third." == snapshot


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
