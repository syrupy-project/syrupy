import json
import os
from contextlib import contextmanager
from difflib import ndiff
from gettext import gettext
from importlib import import_module
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterator,
    Sequence,
)

from .constants import (
    DIFF_LINE_COUNT_LIMIT,
    DIFF_LINE_WIDTH_LIMIT,
    SNAPSHOT_DIRNAME,
    SYMBOL_ELLIPSIS,
)
from .exceptions import FailedToLoadModuleMember


def is_xdist_worker() -> bool:
    worker_name = os.getenv("PYTEST_XDIST_WORKER")
    return bool(worker_name and worker_name != "master")


def is_xdist_controller() -> bool:
    worker_count = os.getenv("PYTEST_XDIST_WORKER_COUNT")
    return bool(worker_count and int(worker_count) > 0 and not is_xdist_worker())


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
        module = import_module(module_name)
    except ModuleNotFoundError:
        raise FailedToLoadModuleMember(
            gettext("Module '{}' does not exist.").format(module_name)
        )

    try:
        return getattr(module, module_member_name)
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


def set_attrs(obj: Any, attrs: Dict[str, Any]) -> Any:
    for k in attrs:
        setattr(obj, k, attrs[k])


@contextmanager
def obj_attrs(obj: Any, attrs: Dict[str, Any]) -> Iterator[None]:
    prev_attrs = {k: getattr(obj, k, None) for k in attrs}
    try:
        yield set_attrs(obj, attrs)
    finally:
        set_attrs(obj, prev_attrs)


def qdiff(
    lines_a: "Sequence[str]",
    lines_b: "Sequence[str]",
    *,
    line_diff_limit: int = DIFF_LINE_COUNT_LIMIT,
    line_size_limit: int = DIFF_LINE_WIDTH_LIMIT,
) -> "Iterator[str]":
    """
    Wrapper around difflib ndiff to bail early
    https://github.com/python/cpython/issues/65452
    """
    first_diff_idx = 0

    for i in range(max(len(lines_a), len(lines_b))):
        if lines_a[i : i + 1] != lines_b[i : i + 1]:  # noqa E203
            first_diff_idx = i
            break

    from_idx = max(first_diff_idx - line_diff_limit, 0)
    to_idx = first_diff_idx + line_diff_limit

    def adjust_line(lines: "Sequence[str]") -> "Sequence[str]":
        symbol_hidden_line = SYMBOL_ELLIPSIS + SYMBOL_ELLIPSIS
        return (
            ([symbol_hidden_line] if from_idx > 0 else [])
            + [
                line[:line_size_limit]
                + (SYMBOL_ELLIPSIS if len(line) > line_size_limit else "")
                for line in lines[from_idx:to_idx]
            ]
            + ([symbol_hidden_line] if to_idx < len(lines) else [])
        )

    return ndiff(adjust_line(lines_a), adjust_line(lines_b))
