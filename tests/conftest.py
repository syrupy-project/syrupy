import pytest

# Constants for testing with extra plugin arguments
_NO_ARGS = []
_XDIST_ZERO = ["--numprocesses", "0"]
_XDIST_TWO = ["--numprocesses", "2"]


@pytest.fixture(
    params=[_NO_ARGS, _XDIST_ZERO, _XDIST_TWO],
    ids=["no_plugin", "xdist_zero", "xdist_two"],
)
def plugin_args(request: pytest.FixtureRequest) -> list[str]:
    """Fixture to test with various plugins"""
    return request.param


@pytest.fixture(
    params=[
        _NO_ARGS,
        _XDIST_ZERO,
        pytest.param(
            _XDIST_TWO,
            marks=pytest.mark.xfail(reason="Not currently compatible with xdist"),
        ),
    ],
    ids=["no_plugin", "xdist_zero", "xdist_two"],
)
def plugin_args_fails_xdist(request: pytest.FixtureRequest) -> list[str]:
    """Fixture to test with various plugins, but expected to fail xdist"""
    return request.param
