import os
from functools import lru_cache
from typing import (
    Any,
    Callable,
    Generator,
)

from .constants import SNAPSHOT_DIRNAME


def in_snapshot_dir(path: str) -> bool:
    parts = path.split(os.path.sep)
    return SNAPSHOT_DIRNAME in parts


@lru_cache(maxsize=128)
def walk_snapshot_dir(root: str) -> Generator[str, None, None]:
    for (dirpath, _, filenames) in os.walk(root):
        if not in_snapshot_dir(dirpath):
            continue
        for filename in filenames:
            if not filename.startswith("."):
                yield os.path.join(dirpath, filename)


def cached_property(f: Callable[..., Any]) -> property:
    return property(lru_cache(maxsize=128)(f))
