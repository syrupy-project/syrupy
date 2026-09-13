"""Unused snapshot detection and removal across pytest-xdist workers.

See https://github.com/syrupy-project/syrupy/issues/535: each worker reports
the snapshots it used and the controller combines them, so unused snapshots are
detected even when the tests that own them ran on a different worker.

Concurrent amber updates under xdist are covered in
``test_xdist_concurrent_amber_update_preserves_all_snapshots`` (#1237).
"""

from pathlib import Path

import pytest


def _write(testdir, params: str) -> None:
    for name in ("test_a", "test_b"):
        Path(testdir.tmpdir, f"{name}.py").write_text(
            "import pytest\n\n"
            f"@pytest.mark.parametrize('i', {params})\n"
            f"def {name}(i, snapshot):\n"
            "    assert i == snapshot\n"
        )


@pytest.fixture
def generated(testdir):
    _write(testdir, "[0, 1, 2, 3]")
    result = testdir.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"8 snapshots generated\.",))
    return testdir


def test_xdist_detects_unused(generated):
    testdir = generated
    # Drop two parametrizations per file, leaving 4 snapshots unused.
    _write(testdir, "[0, 1]")

    result = testdir.runpytest("-v", "--numprocesses", "2")

    result.stdout.re_match_lines((r".*4 snapshots unused\.",))
    assert result.ret != 0


def test_xdist_removes_unused(generated):
    testdir = generated
    _write(testdir, "[0, 1]")

    result = testdir.runpytest("-v", "--numprocesses", "2", "--snapshot-update")

    result.stdout.re_match_lines((r".*4 unused snapshots deleted\.",))
    assert result.ret == 0

    # Partial removal within each shared file: used snapshots are kept.
    content = Path(testdir.tmpdir, "__snapshots__", "test_a.ambr").read_text()
    assert "test_a[0]" in content
    assert "test_a[1]" in content
    assert "test_a[2]" not in content
    assert "test_a[3]" not in content


def test_xdist_disable_unused(generated):
    testdir = generated
    _write(testdir, "[0, 1]")

    result = testdir.runpytest("-v", "--numprocesses", "2", "--snapshot-disable-unused")

    result.stdout.re_match_lines(
        (
            (
                r".*Unused snapshot detection is disabled "
                r"\(--snapshot-disable-unused\)\. This is not recommended\."
            ),
        )
    )
    result.stdout.no_fnmatch_line("*snapshots unused*")
    assert result.ret == 0


def test_without_xdist_installed(testdir):
    """
    Registering the pytest-xdist hook `pytest_testnodedown` unconditionally
    makes pytest raise a `PluginValidationError` when pytest-xdist is not
    installed alongside syrupy, since pytest-xdist provides the hookspec that
    hook implements.

    Simulate pytest-xdist not being installed by disabling the plugin outright
    with `-p no:xdist`.
    """
    testdir.makepyfile(
        """
        def test_a(snapshot):
            assert 1 == snapshot
        """
    )

    result = testdir.runpytest("-p", "no:xdist", "--snapshot-update")

    assert result.ret == 0
    result.stdout.no_fnmatch_line("*PluginValidationError*")
    result.stdout.no_fnmatch_line("*unknown hook*")


def test_p_xdist(testdir, monkeypatch):
    """Test detecting pytest-xdist registered via "-p xdist"."""
    testdir.makepyfile(
        """
        def test_a(snapshot):
            assert 1 == snapshot
        """
    )

    monkeypatch.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
    monkeypatch.setenv("PYTEST_PLUGINS", "syrupy")
    result = testdir.runpytest(
        "-v", "-p", "xdist", "--numprocesses", "2", "--snapshot-update"
    )
    result.stdout.re_match_lines((r"1 snapshot generated",))
    assert result.ret == 0


def test_pytest_plugins_xdist(testdir, monkeypatch):
    """Test detecting pytest-xdist registered via PYTEST_PLUGINS."""
    testdir.makepyfile(
        """
        def test_a(snapshot):
            assert 1 == snapshot
        """
    )

    monkeypatch.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
    monkeypatch.setenv("PYTEST_PLUGINS", "syrupy,xdist.plugin")
    result = testdir.runpytest("-v", "--numprocesses", "2", "--snapshot-update")
    result.stdout.re_match_lines((r"1 snapshot generated",))
    assert result.ret == 0


def test_xdist_concurrent_amber_update_preserves_all_snapshots(testdir):
    """
    Regression for https://github.com/syrupy-project/syrupy/issues/1237.

    When multiple xdist workers --snapshot-update the same multi-entry .ambr
    file, unsynchronized read-modify-write used to silently drop snapshots
    while still reporting a full successful update. File locking is enabled
    automatically under xdist.
    """
    n = 200
    testdir.makepyfile(
        test_race=f"""
        import pytest

        VALUE = "v1"

        @pytest.mark.parametrize("i", range({n}))
        def test_many(snapshot, i):
            assert f"{{VALUE}}-{{i}}" == snapshot
        """
    )

    result = testdir.runpytest("-q", "--snapshot-update")
    result.stdout.re_match_lines((rf"{n} snapshots generated\.",))
    assert result.ret == 0

    ambr = Path(testdir.tmpdir, "__snapshots__", "test_race.ambr")
    assert ambr.read_text().count("# name:") == n

    Path(testdir.tmpdir, "test_race.py").write_text(
        f"""
import pytest

VALUE = "v2"

@pytest.mark.parametrize("i", range({n}))
def test_many(snapshot, i):
    assert f"{{VALUE}}-{{i}}" == snapshot
"""
    )

    result = testdir.runpytest(
        "-q",
        "--snapshot-update",
        "--numprocesses",
        "8",
        "--dist",
        "load",
    )
    result.stdout.re_match_lines((rf"{n} snapshots updated\.",))
    assert result.ret == 0
    content = ambr.read_text()
    assert content.count("# name:") == n
    for i in range(n):
        assert f"test_many[{i}]" in content

    lock_path = Path(str(ambr) + ".lock")
    tmp_path = Path(str(ambr) + ".tmp")
    assert not lock_path.exists()
    assert not tmp_path.exists()


def test_xdist_update_cleans_up_write_sidecars(testdir):
    """Under xdist, amber updates must not leave lock/tmp files after the run."""
    n = 20
    testdir.makepyfile(
        test_sidecars=f"""
        import pytest

        @pytest.mark.parametrize("i", range({n}))
        def test_many(snapshot, i):
            assert f"v1-{{i}}" == snapshot
        """
    )

    result = testdir.runpytest(
        "-q",
        "--snapshot-update",
        "--numprocesses",
        "4",
        "--dist",
        "load",
    )
    result.stdout.re_match_lines((rf"{n} snapshots generated\.",))
    assert result.ret == 0

    ambr = Path(testdir.tmpdir, "__snapshots__", "test_sidecars.ambr")
    assert ambr.exists()
    assert not Path(str(ambr) + ".lock").exists()
    assert not Path(str(ambr) + ".tmp").exists()


def test_without_xdist_update_does_not_create_sidecars(testdir):
    """Single-process updates must not create lock/tmp sidecars."""
    testdir.makepyfile(
        test_nlock="""
        def test_a(snapshot):
            assert 1 == snapshot
        """
    )
    result = testdir.runpytest("-q", "--snapshot-update", "-p", "no:xdist")
    assert result.ret == 0
    ambr = Path(testdir.tmpdir, "__snapshots__", "test_nlock.ambr")
    assert ambr.exists()
    assert not Path(str(ambr) + ".lock").exists()
    assert not Path(str(ambr) + ".tmp").exists()
