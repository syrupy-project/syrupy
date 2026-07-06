"""Unused snapshot detection and removal across pytest-xdist workers.

See https://github.com/syrupy-project/syrupy/issues/535: each worker reports
the snapshots it used and the controller combines them, so unused snapshots are
detected even when the tests that own them ran on a different worker.
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
