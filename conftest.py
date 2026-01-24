import pytest

from syrupy.utils import env_context

pytest_plugins = "pytester"


@pytest.fixture
def osenv():
    return env_context
