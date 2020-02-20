from pathlib import Path
from typing import Generator

from .constants import SNAPSHOT_DIRNAME


def in_snapshot_dir(path: Path) -> bool:
    return SNAPSHOT_DIRNAME in path.parts


def walk_snapshot_dir(root: str) -> Generator[str, None, None]:
    for filepath in Path(root).rglob("*"):
        if not in_snapshot_dir(filepath):
            continue
        if not filepath.name.startswith(".") and filepath.is_file():
            yield str(filepath)
