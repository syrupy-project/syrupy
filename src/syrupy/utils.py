"""
Syrupy utility methods
"""

import os
from typing import Generator

from .constants import SNAPSHOT_DIRNAME


def in_snapshot_dir(path: str) -> bool:
    """
    Verify if path is in a snapshot directory
    """
    parts = path.split(os.path.sep)
    return SNAPSHOT_DIRNAME in parts


def walk_snapshot_dir(root: str) -> Generator[str, None, None]:
    """
    Traverse all the files in root folder
    """
    for (dirpath, _, filenames) in os.walk(root):
        if not in_snapshot_dir(dirpath):
            continue
        for filename in filenames:
            if not filename.startswith("."):
                yield os.path.join(dirpath, filename)
