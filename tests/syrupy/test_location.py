from pathlib import Path
from unittest.mock import MagicMock

import pytest

from syrupy.constants import PYTEST_NODE_SEP
from syrupy.extensions.single_file import SingleFileSnapshotExtension
from syrupy.location import PyTestLocation


def mock_pytest_item(node_id: str, method_name: str) -> "pytest.Item":
    mock_node = MagicMock(spec=pytest.Item)
    mock_node.nodeid = node_id
    [filepath, *_, nodename] = node_id.split(PYTEST_NODE_SEP)
    mock_node.name = nodename
    mock_node.path = Path(filepath)
    mock_node.obj = MagicMock()
    mock_node.obj.__module__ = Path(filepath).stem
    mock_node.obj.__name__ = method_name
    return mock_node


@pytest.mark.parametrize(
    "node_id, method_name, expected_filename, expected_classname, expected_snapshotname",
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
    assert location.basename == expected_filename
    assert location.snapshot_name == expected_snapshotname


@pytest.mark.parametrize(
    "node_id, method_name,"
    "expected_location_matches, expected_location_misses,"
    "expected_snapshot_matches, expected_snapshot_misses",
    (
        (
            "/tests/module/test_file.py::TestClass::method_name",
            "method_name",
            (
                "/tests/module/test_file.snap",
                "/tests/module/__snapshots__/test_file",
                "/tests/module/test_file/1.snap",
            ),
            (
                "test.snap",
                "__others__/test/file.snap",
                "test_file_extra.snap",
                "__snapshots__/test_file_extra",
                "test_file_extra/1.snap",
                "test_file/extra/1.snap",
                "__snapshots__/test_file/extra/even/more/1.snap",
                "/tests/other/__snapshots__/test_file",
            ),
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
            (
                "/tests/module/test_file.snap",
                "/tests/module/__snapshots__/test_file",
                "/tests/module/test_file/TestClass.method_name[1].snap",
                "/tests/module/test_file/TestClass.method_name[1].1.snap",
                "/tests/module/test_file/TestClass.method_name[1][1].snap",
            ),
            (
                "test.snap",
                "__others__/test/file.snap",
                "test_file_extra.snap",
                "__snapshots__/test_file_extra",
                "test_file_extra/1.snap",
                "test_file/extra/1.snap",
                "__snapshots__/test_file/extra/even/more/1.snap",
                "test_file/TestClass.method_name[1]xyz.snap",
                "test_file/TestClass.method_name[2].snap",
                "/tests/other/__snapshots__/test_file",
            ),
            (
                "TestClass.method_name",
                "TestClass.method_name[1]",
                "TestClass.method_name.1",
                "TestClass.method_name[1][1]",
                "TestClass.method_name[1].1",
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


def test_location_does_not_match_same_basename_in_other_directory():
    module_a_views_snapshot = "/project/module_a/tests/__snapshots__/test_views.ambr"
    module_b_test = mock_pytest_item(
        "/project/module_b/tests/test_views.py::test_module_b_view",
        "test_module_b_view",
    )
    location = PyTestLocation(module_b_test)

    assert not location.matches_snapshot_location(module_a_views_snapshot)


def test_location_matches_snapshot_in_same_directory():
    module_a_views_snapshot = "/project/module_a/tests/__snapshots__/test_views.ambr"
    module_a_test = mock_pytest_item(
        "/project/module_a/tests/test_views.py::test_module_a_view",
        "test_module_a_view",
    )
    location = PyTestLocation(module_a_test)

    assert location.matches_snapshot_location(module_a_views_snapshot)


def test_location_does_not_match_prefix_basename_in_snapshot_stem():
    """
    Regression for #596 / PR #607: ``test_config`` must not match
    ``test_config_entries`` snapshot files.
    """
    location = PyTestLocation(
        mock_pytest_item("/tests/test_config.py::test_config", "test_config")
    )

    assert not location.matches_snapshot_location(
        "/tests/snapshots/test_config_entries.ambr"
    )


def test_location_parametrized_single_file_snapshot_in_test_site():
    """
    Regression for #918 / PR #965: parametrized single-file snapshots must still
    match paths under their test file's directory.
    """
    location = PyTestLocation(
        mock_pytest_item(
            "/tests/module/test_file.py::TestClass::method_name[1]",
            "method_name",
        )
    )

    assert location.matches_snapshot_location(
        "/tests/module/test_file/TestClass.method_name[1].snap"
    )


class _MultiDotExtension(SingleFileSnapshotExtension):
    file_extension = "custom.raw"


def _parametrized_location(node_id: str) -> PyTestLocation:
    return PyTestLocation(mock_pytest_item(node_id, "test_long"))


def _single_file_path(basename: str, extension: str = "raw") -> str:
    suffix = f".{extension}" if extension else ""
    return f"/tests/module/__snapshots__/test_file/{basename}{suffix}"


def test_truncated_parametrized_single_file_snapshot_matches_its_test():
    """A 255-character single-file snapshot belongs to the id that produced it."""
    long_id = "a" * 300
    long_location = _parametrized_location(
        f"/tests/module/test_file.py::test_long[{long_id}]"
    )
    short_location = _parametrized_location("/tests/module/test_file.py::test_long[a]")
    other_location = _parametrized_location(
        f"/tests/module/test_file.py::test_long[{'b' * 300}]"
    )

    basename = SingleFileSnapshotExtension.get_snapshot_name(
        test_location=long_location
    )
    assert len(basename) + len(".raw") == 255
    snapshot = _single_file_path(basename)

    assert SingleFileSnapshotExtension.matches_test_location(
        test_location=long_location, snapshot_location=snapshot
    )
    assert not SingleFileSnapshotExtension.matches_test_location(
        test_location=short_location, snapshot_location=snapshot
    )
    assert not SingleFileSnapshotExtension.matches_test_location(
        test_location=other_location, snapshot_location=snapshot
    )
    assert not SingleFileSnapshotExtension.matches_test_location(
        test_location=long_location,
        snapshot_location=f"/tests/other/__snapshots__/test_file/{basename}.raw",
    )


def test_truncated_multipart_extension_does_not_match_as_raw():
    long_location = _parametrized_location(
        f"/tests/module/test_file.py::test_long[{'a' * 300}]"
    )
    basename = _MultiDotExtension.get_snapshot_name(test_location=long_location)
    assert len(basename) + len(".custom.raw") == 255
    snapshot = _single_file_path(basename, "custom.raw")

    assert _MultiDotExtension.matches_test_location(
        test_location=long_location, snapshot_location=snapshot
    )
    assert not SingleFileSnapshotExtension.matches_test_location(
        test_location=long_location, snapshot_location=snapshot
    )


def test_sanitized_truncated_name_matches_stored_stem():
    dirty_location = _parametrized_location(
        f"/tests/module/test_file.py::test_long[a?{'b' * 300}]"
    )
    basename = SingleFileSnapshotExtension.get_snapshot_name(
        test_location=dirty_location
    )
    assert "?" not in basename
    assert SingleFileSnapshotExtension.matches_test_location(
        test_location=dirty_location,
        snapshot_location=_single_file_path(basename),
    )


def test_untruncated_parametrized_single_file_snapshot_still_matches():
    short_location = _parametrized_location("/tests/module/test_file.py::test_long[a]")
    basename = SingleFileSnapshotExtension.get_snapshot_name(
        test_location=short_location
    )
    assert SingleFileSnapshotExtension.matches_test_location(
        test_location=short_location,
        snapshot_location=_single_file_path(basename),
    )
    assert SingleFileSnapshotExtension.matches_test_location(
        test_location=short_location,
        snapshot_location=_single_file_path(f"{basename}.1"),
    )
