from unittest.mock import patch, NonCallableMock

import pytest
from syrupy.constants import DISABLE_COLOR_ENV_VAR
from syrupy.terminal import (
    reset,
    red,
    yellow,
    green,
    bold,
    error_style,
    warning_style,
    success_style,
    snapshot_style,
    snapshot_diff_style,
    received_style,
    received_diff_style,
    context_style,
)


def test_colors_off_does_not_call_colored():
    """
    Test that disabling colors prevents instantiating colored object.
    Enables workarounds for when instantiating the colored object causes crashes,
    see issue #633
    """

    with patch('colored.colored.__init__', new_callable=NonCallableMock):
        with patch.dict('os.environ', {DISABLE_COLOR_ENV_VAR: 'true'}):
            for method in (
                reset,
                red,
                yellow,
                green,
                bold,
                error_style,
                warning_style,
                success_style,
                snapshot_style,
                snapshot_diff_style,
                received_style,
                received_diff_style,
                context_style,
            ):
                _ = method("foo")
        
        # Prevent test from accidentally passing by patching wrong object
        with pytest.raises(TypeError) as excinfo:
            _ = red("foo")
        
        assert 'NonCallableMock' in str(excinfo.value)
