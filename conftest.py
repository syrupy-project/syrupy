import os
from collections.abc import Iterator
from contextlib import contextmanager

import pytest

pytest_plugins = "pytester"


@contextmanager
def _env_context(**kwargs: str) -> Iterator[None]:
    prev_env = {**os.environ}
    try:
        yield os.environ.update(kwargs)
    finally:
        os.environ.clear()
        os.environ.update(prev_env)


@pytest.fixture
def osenv():
    return _env_context
