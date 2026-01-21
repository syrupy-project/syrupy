import pytest

from syrupy.utils import env_context

# This was some kind of hack, which is quite unsavory.
# I commented to avoid circular imports during type checking.

# typing.TYPE_CHECKING = True
pytest_plugins = "pytester"


@pytest.fixture
def osenv():
    return env_context
