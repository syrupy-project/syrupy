import pytest

# Constants for testing with extra plugin arguments
_NO_ARGS = []
_XDIST_ARGS = ["--numprocesses", "auto"]


@pytest.fixture(
    params=[
        _NO_ARGS,
        pytest.param(
            _XDIST_ARGS,
            marks=pytest.mark.xfail(reason="Not currently compatible with xdist"),
        ),
    ],
    ids=["no_plugin", "with_xdist"],
)
def plugin_args(request: pytest.FixtureRequest) -> list[str]:
    """Fixture to test with various plugins"""
    return request.param
