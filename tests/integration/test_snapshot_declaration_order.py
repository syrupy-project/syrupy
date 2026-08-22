"""Tests for experimental --snapshot-declaration-order (#968)."""

from pathlib import Path


def _parametrized_with_ids() -> str:
    return """
        import pytest

        @pytest.mark.parametrize(
            "value",
            ["test_b", "test_a"],
            ids=["b", "a"],
        )
        def test_input(value, snapshot):
            assert value == snapshot
        """


def _parametrized_without_ids() -> str:
    return """
        import pytest

        @pytest.mark.parametrize("value", ["z", "a"])
        def test_input(value, snapshot):
            assert value == snapshot
        """


def _non_parametrized_out_of_alpha_order() -> str:
    return """
        def test_zebra(snapshot):
            assert "z" == snapshot

        def test_apple(snapshot):
            assert "a" == snapshot
        """


def _snapshot_names_in_order(snapshot_file: Path) -> list[str]:
    names: list[str] = []
    for line in snapshot_file.read_text().splitlines():
        if line.startswith("# name:"):
            names.append(line.split(":", 1)[1].strip())
    return names


def test_default_orders_snapshots_alphabetically(pytester):
    # File contents are asserted here; skip xdist because workers racing on the
    # same .ambr file can drop siblings (pre-existing amber write race, unrelated
    # to declaration-order sorting).
    pytester.makepyfile(test_input=_parametrized_with_ids())
    result = pytester.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    assert result.ret == 0

    snapshot_file = pytester.path / "__snapshots__" / "test_input.ambr"
    assert _snapshot_names_in_order(snapshot_file) == [
        "test_input[a]",
        "test_input[b]",
    ]


def test_declaration_order_with_parametrize_ids(pytester):
    pytester.makepyfile(test_input=_parametrized_with_ids())
    result = pytester.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-declaration-order",
    )
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    assert result.ret == 0

    snapshot_file = pytester.path / "__snapshots__" / "test_input.ambr"
    assert _snapshot_names_in_order(snapshot_file) == [
        "test_input[b]",
        "test_input[a]",
    ]


def test_declaration_order_without_parametrize_ids(pytester):
    pytester.makepyfile(test_input=_parametrized_without_ids())
    result = pytester.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-declaration-order",
    )
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    assert result.ret == 0

    snapshot_file = pytester.path / "__snapshots__" / "test_input.ambr"
    assert _snapshot_names_in_order(snapshot_file) == [
        "test_input[z]",
        "test_input[a]",
    ]


def test_declaration_order_for_non_parametrized_tests(pytester):
    pytester.makepyfile(test_order=_non_parametrized_out_of_alpha_order())
    result = pytester.runpytest(
        "-v",
        "--snapshot-update",
        "--snapshot-declaration-order",
    )
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    assert result.ret == 0

    snapshot_file = pytester.path / "__snapshots__" / "test_order.ambr"
    assert _snapshot_names_in_order(snapshot_file) == [
        "test_zebra",
        "test_apple",
    ]


def test_default_orders_non_parametrized_alphabetically(pytester):
    pytester.makepyfile(test_order=_non_parametrized_out_of_alpha_order())
    result = pytester.runpytest("-v", "--snapshot-update")
    result.stdout.re_match_lines((r"2 snapshots generated\.",))
    assert result.ret == 0

    snapshot_file = pytester.path / "__snapshots__" / "test_order.ambr"
    assert _snapshot_names_in_order(snapshot_file) == [
        "test_apple",
        "test_zebra",
    ]
