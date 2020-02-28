from importlib import import_module
from pathlib import Path
from typing import (
    Any,
    Generator,
)

from .constants import SNAPSHOT_DIRNAME


def in_snapshot_dir(path: Path) -> bool:
    return SNAPSHOT_DIRNAME in path.parts


def walk_snapshot_dir(root: str) -> Generator[str, None, None]:
    for filepath in Path(root).rglob("*"):
        if not in_snapshot_dir(filepath):
            continue
        if not filepath.name.startswith(".") and filepath.is_file():
            yield str(filepath)


class FailedToLoadModuleMember(Exception):
    pass


def load_module_member_from_path(path: str) -> Any:
    path_parts = path.split(".")

    module_name = ".".join(path_parts[:-1])
    module_member_name = path_parts[-1:][0]

    if not module_name:
        raise FailedToLoadModuleMember(
            f"Cannot load member '{module_member_name}' without module path"
        )

    try:
        module = import_module(module_name)
    except ModuleNotFoundError:
        raise FailedToLoadModuleMember(f"Module '{module_name}' does not exist.")

    try:
        module_member = getattr(module, module_member_name)
    except AttributeError:
        raise FailedToLoadModuleMember(
            f"Member '{module_member_name}' not found in module '{module_name}'."
        )

    return module_member
