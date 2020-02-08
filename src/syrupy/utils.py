from pathlib import Path
from typing import Generator

from .constants import SNAPSHOT_DIRNAME


def in_snapshot_dir(path: Path) -> bool:
    return SNAPSHOT_DIRNAME in path.parts


def walk_snapshot_dir(root: str) -> Generator[str, None, None]:
    if not Path(root).exists():
        return

    for file_path in Path(root).rglob("*"):
        if not in_snapshot_dir(file_path):
            continue
        if not file_path.name.startswith(".") and file_path.is_file():
            yield str(file_path)
