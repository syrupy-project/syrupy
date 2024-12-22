import pytest

_TEST = """
def test_foo(snapshot):
    assert {**base} == snapshot(name="a")
    assert {**base, **extra} == snapshot(name="b", diff="a")
"""


def _make_file(testdir, base, extra):
    testdir.makepyfile(
        test_file="\n\n".join([f"base = {base!r}", f"extra = {extra!r}", _TEST])
    )


def _run_test(testdir, base, extra, expected_update_lines):
    _make_file(testdir, base=base, extra=extra)

    # Run with --snapshot-update, to generate/update snapshots:
    result = testdir.runpytest(
        "-v",
        "--snapshot-update",
    )
    result.stdout.re_match_lines((expected_update_lines,))
    assert result.ret == 0

    # Run without --snapshot-update, to validate the snapshots are actually up-to-date
    result = testdir.runpytest("-v")
    result.stdout.re_match_lines((r"2 snapshots passed\.",))
    assert result.ret == 0


def test_diff_lifecycle(testdir) -> pytest.Testdir:
    # first: create both snapshots completely from scratch
    _run_test(
        testdir,
        base={"A": 1},
        extra={"X": 10},
        expected_update_lines=r"2 snapshots generated\.",
    )

    # second: edit the base data, to change the data for both snapshots (only changes the serialized output for the base snapshot `a`).
    _run_test(
        testdir,
        base={"A": 1, "B": 2},
        extra={"X": 10},
        expected_update_lines=r"1 snapshot passed. 1 snapshot updated\.",
    )

    # third: edit just the extra data (only changes the serialized output for the diff snapshot `b`)
    _run_test(
        testdir,
        base={"A": 1, "B": 2},
        extra={"X": 10, "Y": 20},
        expected_update_lines=r"1 snapshot passed. 1 snapshot updated\.",
    )
