import json
import os
from contextlib import contextmanager
from gettext import gettext
from importlib import import_module
from pathlib import Path
from typing import (
    Any,
    Iterator,
)

from .constants import SNAPSHOT_DIRNAME
from .exceptions import FailedToLoadModuleMember


def in_snapshot_dir(path: Path) -> bool:
    return SNAPSHOT_DIRNAME in path.parts


def walk_snapshot_dir(root: str) -> Iterator[str]:
    for filepath in Path(root).rglob("*"):
        if not in_snapshot_dir(filepath):
            continue
        if not filepath.name.startswith(".") and filepath.is_file():
            yield str(filepath)


def import_module_member(path: str) -> Any:
    sep = "."
    [*module_parts, module_member_name] = path.split(sep)
    module_name = sep.join(module_parts)

    if not module_name:
        raise FailedToLoadModuleMember(
            gettext("Cannot load member '{}' without module path").format(
                module_member_name,
            )
        )
    try:
        return getattr(import_module(module_name), module_member_name)
    except ModuleNotFoundError:
        raise FailedToLoadModuleMember(
            gettext("Module '{}' does not exist.").format(module_name)
        )
    except AttributeError:
        raise FailedToLoadModuleMember(
            gettext("Member '{}' not found in module '{}'.").format(
                module_member_name,
                module_name,
            )
        )


def get_env_value(env_var_name: str) -> object:
    try:
        return json.loads(os.environ[env_var_name])
    except (KeyError, TypeError, json.decoder.JSONDecodeError):
        return os.environ.get(env_var_name)


@contextmanager
def env_context(**kwargs: str) -> Iterator[None]:
    prev_env = {**os.environ}
    try:
        yield os.environ.update(kwargs)
    finally:
        os.environ.clear()
        os.environ.update(prev_env)
