import os

from syrupy.terminal import (
    _is_color_disabled as is_color_disabled,
)
from syrupy.terminal import (
    disable_color,
    snapshot_style,
)


def test_disable_color_context_toggles_styling():
    assert is_color_disabled() is False
    styled = snapshot_style("hello")
    assert styled != "hello"  # contains ANSI escape codes

    with disable_color():
        assert is_color_disabled() is True
        assert snapshot_style("hello") == "hello"

    # Restored after the context exits.
    assert is_color_disabled() is False
    assert snapshot_style("hello") == styled


def test_disable_color_does_not_mutate_environ():
    """Color suppression must not touch os.environ (not thread safe)."""
    before = dict(os.environ)
    with disable_color():
        assert dict(os.environ) == before
    assert dict(os.environ) == before


def test_external_no_color_env_var_disables_color(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "true")
    assert is_color_disabled() is True
    assert snapshot_style("hello") == "hello"
