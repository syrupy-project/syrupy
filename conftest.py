import typing

import pytest

from syrupy.utils import env_context

typing.TYPE_CHECKING = True
pytest_plugins = "pytester"


@pytest.fixture
def osenv():
    return env_context
