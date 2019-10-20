import pytest

def test_simple_string(snapshot):
    assert snapshot("Lorem ipsum.")


def test_raw_string(snapshot):
    assert snapshot(r"Raw string")


def test_multiple_snapshots(snapshot):
    assert snapshot("First.")
    assert snapshot("Second.")

@pytest.mark.parametrize("expected", [r"Escaped \n", r"Backslash \u U"])
def test_parametrized_with_special_char(snapshot, expected):
    assert snapshot(expected)
