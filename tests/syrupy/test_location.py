from pathlib import Path
from unittest.mock import MagicMock

import pytest

from syrupy.location import PyTestLocation


def mock_pytest_item(node_id: str, method_name: str) -> "pytest.Item":
    mock_node = MagicMock(spec=pytest.Item)
    mock_node.nodeid = node_id
    [filepath, *_, nodename] = node_id.split("::")
    mock_node.name = nodename
    mock_node.fspath = filepath
    mock_node.obj = MagicMock()
    mock_node.obj.__module__ = Path(filepath).stem
    mock_node.obj.__name__ = method_name
    return mock_node


@pytest.mark.parametrize(
    "node_id, method_name, expected_filename,"
    "expected_classname,expected_snapshotname",
    (
        (
            "/tests/module/test_file.py::TestClass::method_name",
            "method_name",
            "test_file",
            "TestClass",
            "TestClass.method_name",
        ),
        (
            "/tests/module/test_file.py::TestClass::method_name[1]",
            "method_name",
            "test_file",
            "TestClass",
            "TestClass.method_name[1]",
        ),
        (
            "/tests/module/nest/test_file.py::TestClass::TestSubClass::method_name",
            "method_name",
            "test_file",
            "TestClass.TestSubClass",
            "TestClass.TestSubClass.method_name",
        ),
    ),
)
def test_location_properties(
    node_id,
    method_name,
    expected_filename,
    expected_classname,
    expected_snapshotname,
):
    location = PyTestLocation(mock_pytest_item(node_id, method_name))
    assert location.classname == expected_classname
    assert location.filename == expected_filename
    assert location.snapshot_name == expected_snapshotname


@pytest.mark.parametrize(
    "node_id, method_name,"
    "expected_location_matches, expected_location_misses,"
    "expected_snapshot_matches, expected_snapshot_misses",
    (
        (
            "/tests/module/test_file.py::TestClass::method_name",
            "method_name",
            ("test_file.snap", "__snapshots__/test_file", "test_file/1.snap"),
            ("test.snap", "__others__/test/file.snap"),
            (
                "TestClass.method_name",
                "TestClass.method_name[1]",
                "TestClass.method_name.1",
            ),
            ("method_name", "TestClass.method_names"),
        ),
        (
            "/tests/module/test_file.py::TestClass::method_name[1]",
            "method_name",
            ("test_file.snap", "__snapshots__/test_file", "test_file/1.snap"),
            ("test.snap", "__others__/test/file.snap"),
            (
                "TestClass.method_name",
                "TestClass.method_name[1]",
                "TestClass.method_name.1",
            ),
            ("method_name", "TestClass.method_names"),
        ),
    ),
)
def test_location_matching(
    node_id,
    method_name,
    expected_location_matches,
    expected_location_misses,
    expected_snapshot_matches,
    expected_snapshot_misses,
):
    location = PyTestLocation(mock_pytest_item(node_id, method_name))

    for location_match in expected_location_matches:
        assert location.matches_snapshot_location(location_match)

    for location_miss in expected_location_misses:
        assert not location.matches_snapshot_location(location_miss)

    for snapshot_match in expected_snapshot_matches:
        assert location.matches_snapshot_name(snapshot_match)

    for snapshot_miss in expected_snapshot_misses:
        assert not location.matches_snapshot_name(snapshot_miss)
