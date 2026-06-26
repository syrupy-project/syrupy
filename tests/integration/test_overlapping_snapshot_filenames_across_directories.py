"""
Regression tests for overlapping snapshot filenames in different directories.

- https://github.com/syrupy-project/syrupy/issues/1079
- https://github.com/syrupy-project/syrupy/issues/918 (fixed in #965)
"""

import pytest

MODULE_A_TEST_FOO = """
def test_module_a_foo(snapshot):
    result = {"module": "a", "type": "foo", "status": "ok"}
    assert result == snapshot
"""

MODULE_A_TEST_VIEWS = """
def test_module_a_view(snapshot):
    result = {"module": "a", "type": "view", "status": "ok"}
    assert result == snapshot
"""

MODULE_B_TEST_VIEWS = """
def test_module_b_view(snapshot):
    result = {"module": "b", "type": "view", "status": "ok"}
    assert result == snapshot
"""


def _write_project(pytester: pytest.Pytester) -> None:
    pytester.mkdir("module_a")
    pytester.mkdir("module_b")
    module_a_tests = pytester.mkdir("module_a/tests")
    module_b_tests = pytester.mkdir("module_b/tests")

    (pytester.path / "module_a" / "__init__.py").write_text("", encoding="utf-8")
    (pytester.path / "module_b" / "__init__.py").write_text("", encoding="utf-8")
    (module_a_tests / "__init__.py").write_text("", encoding="utf-8")
    (module_b_tests / "__init__.py").write_text("", encoding="utf-8")

    (module_a_tests / "test_foo.py").write_text(MODULE_A_TEST_FOO, encoding="utf-8")
    (module_a_tests / "test_views.py").write_text(MODULE_A_TEST_VIEWS, encoding="utf-8")
    (module_b_tests / "test_views.py").write_text(MODULE_B_TEST_VIEWS, encoding="utf-8")


@pytest.fixture
def overlapping_snapshot_project(pytester: pytest.Pytester) -> pytest.Pytester:
    _write_project(pytester)
    result = pytester.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"3 snapshots generated\.",))
    assert result.ret == 0
    return pytester


def test_partial_run_does_not_report_unrelated_same_basename_snapshots(
    overlapping_snapshot_project: pytest.Pytester,
    plugin_args: list[str],
) -> None:
    """
    Running a subset of tests across modules must not flag snapshots from
    untargeted test files that merely share a basename in another directory.
    """
    result = overlapping_snapshot_project.runpytest(
        "-v",
        "--snapshot-details",
        "module_a/tests/test_foo.py",
        "module_b/tests/test_views.py",
        *plugin_args,
    )
    result.stdout.re_match_lines((r"2 snapshots passed\.",))
    result.stdout.no_re_match_line(
        r"Unused test_module_a_view "
        r"\(module_a[\\/]tests[\\/]__snapshots__[\\/]test_views\.ambr\)"
    )
    assert result.ret == 0


TEST_CONFIG = """
def test_config(snapshot):
    assert {"scope": "root"} == snapshot
"""

TEST_CONFIG_ENTRIES_ROOT = """
def test_config_entries(snapshot):
    assert {"scope": "root", "type": "entries"} == snapshot
"""

TEST_CONFIG_ENTRIES_COMPONENT = """
def test_config_entries(snapshot):
    assert {"scope": "component", "type": "entries"} == snapshot
"""


def _write_nested_project(pytester: pytest.Pytester) -> None:
    pytester.mkdir("test_root")
    pytester.mkdir("test_root/components")
    component_config = pytester.mkdir("test_root/components/config")

    (pytester.path / "test_root" / "test_config.py").write_text(
        TEST_CONFIG, encoding="utf-8"
    )
    (pytester.path / "test_root" / "test_config_entries.py").write_text(
        TEST_CONFIG_ENTRIES_ROOT, encoding="utf-8"
    )
    (component_config / "test_config_entries.py").write_text(
        TEST_CONFIG_ENTRIES_COMPONENT, encoding="utf-8"
    )


@pytest.fixture
def nested_snapshot_project(pytester: pytest.Pytester) -> pytest.Pytester:
    pytester.makeini(
        """
        [pytest]
        addopts = --import-mode=importlib
        """
    )
    _write_nested_project(pytester)
    result = pytester.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"3 snapshots generated\.",))
    assert result.ret == 0
    return pytester


def test_partial_run_does_not_report_unrelated_nested_same_basename_snapshots(
    nested_snapshot_project: pytest.Pytester,
    plugin_args: list[str],
) -> None:
    """
    Regression for #918: a nested test file must not cause an unrelated snapshot
    file with the same basename in a parent directory to be marked unused.

    Mirrors Home Assistant's layout where ``tests/snapshots/test_config_entries.ambr``
    must be ignored when only ``tests/components/config/test_config_entries.py`` and
    ``tests/test_config.py`` are targeted.
    """
    result = nested_snapshot_project.runpytest(
        "-v",
        "--snapshot-details",
        "test_root/components/config/test_config_entries.py",
        "test_root/test_config.py",
        *plugin_args,
    )
    result.stdout.re_match_lines((r"2 snapshots passed\.",))
    result.stdout.no_re_match_line(
        r"Unused test_config_entries "
        r"\(test_root[\\/]__snapshots__[\\/]test_config_entries\.ambr\)"
    )
    assert result.ret == 0
