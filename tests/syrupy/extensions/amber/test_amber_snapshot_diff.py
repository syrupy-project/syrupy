from types import MappingProxyType

import pytest


def test_snapshot_diff(snapshot):
    my_dict = {
        "field_0": True,
        "field_1": "no_value",
        "nested": {
            "field_0": 1,
        },
    }
    assert my_dict == snapshot
    my_dict["field_1"] = "yes_value"
    assert my_dict == snapshot(diff=0)
    my_dict["nested"]["field_0"] = 2
    assert my_dict == snapshot(diff=0)


def test_snapshot_diff_id(snapshot):
    my_dict = {
        "field_0": True,
        "field_1": "no_value",
        "field_2": 0,
        "field_3": None,
        "field_4": 1,
        "field_5": False,
        "field_6": (True, "hey", 2, None),
        "field_7": {False, "no", 0, None},  # noqa: disable=B033
    }
    dictLargeSnapshot = {
        **my_dict,
        "nested_0": dict(my_dict),
        "nested_1": dict(my_dict),
    }

    assert dictLargeSnapshot == snapshot(name="large snapshot")
    dictDiffLargeSnapshot = {
        **dictLargeSnapshot,
        "field_1": "yes_value",
        "field_6": ("hey", 2, False),
        "field_7": {"yes", 0, None},
    }
    assert dictDiffLargeSnapshot == snapshot(diff="large snapshot")
    dictCase3 = {
        **dictLargeSnapshot,
        "nested_0": MappingProxyType({**my_dict, "field_0": 2}),
        "nested_1": MappingProxyType({**my_dict, "field_0": 2}),
    }
    assert dictCase3 == snapshot(name="case3", diff="large snapshot")


def test_snapshot_no_diff_raises_exception(snapshot):
    my_dict = {
        "field_0": "value_0",
    }
    with pytest.raises(AssertionError, match="SnapshotDoesNotExist"):
        assert my_dict == snapshot(diff="does not exist index")
