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
    List,
    Optional,
    Sequence,
    Union,
)

from .constants import (
    DIFF_LINE_COUNT_LIMIT,
    DIFF_LINE_WIDTH_LIMIT,
    SYMBOL_ELLIPSIS,
)
from .exceptions import FailedToLoadModuleMember


def is_xdist_worker() -> bool:
    worker_name = os.getenv("PYTEST_XDIST_WORKER")
    return bool(worker_name and worker_name != "master")


def is_xdist_controller() -> bool:
    worker_count = os.getenv("PYTEST_XDIST_WORKER_COUNT")
    return bool(worker_count and int(worker_count) > 0 and not is_xdist_worker())


def walk_snapshot_dir(
    root: Union[str, Path], *, ignore_extensions: Optional[List[str]] = None
) -> Iterator[str]:
    ignore_exts: set[str] = set(ignore_extensions or [])

    for filepath in Path(root).rglob("*"):
        if not filepath.name.startswith(".") and filepath.is_file():
            if filepath.suffixes and filepath.suffixes[-1][1:] in ignore_exts:
                continue
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
    except ModuleNotFoundError as e:
        raise FailedToLoadModuleMember(
            gettext("Module '{}' does not exist.").format(module_name)
        ) from e

    try:
        return getattr(module, module_member_name)
    except AttributeError as e:
        raise FailedToLoadModuleMember(
            gettext("Member '{}' not found in module '{}'.").format(
                module_member_name,
                module_name,
            )
        ) from e


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
    first_diff_line_idx = 0
    first_diff_char_idx = 0

    for i in range(max(len(lines_a), len(lines_b))):
        line_a = "".join(lines_a[i : i + 1])  # noqa E203
        line_b = "".join(lines_b[i : i + 1])  # noqa E203
        if line_a != line_b:
            first_diff_line_idx = i
            for j in range(max(len(line_a), len(line_b))):
                char_a = line_a[j : j + 1]  # noqa E203
                char_b = line_b[j : j + 1]  # noqa E203
                if char_a != char_b:
                    first_diff_char_idx = j
                    break
            break

    def adjust_lines(lines: "Sequence[str]") -> "Sequence[str]":
        line_idx_from = max(first_diff_line_idx - line_diff_limit, 0)
        line_idx_to = first_diff_line_idx + line_diff_limit

        symbol_hidden_line = SYMBOL_ELLIPSIS + SYMBOL_ELLIPSIS
        return (
            # include an indicator in the diff if this was not the first line
            ([symbol_hidden_line] if line_idx_from > 0 else [])
            # show included lines with the ends truncated off
            + [
                adj_line
                for n, line in enumerate(lines[line_idx_from:line_idx_to])
                # adjust the first line shown to be from the first different spotted
                for line_start, line_end in [
                    (
                        (
                            max(first_diff_char_idx - line_size_limit, 0)
                            if n == line_idx_from
                            else 0
                        ),
                        (
                            first_diff_char_idx + line_size_limit
                            if n == line_idx_from
                            else line_size_limit
                        ),
                    ),
                ]
                for adj_line in [
                    (SYMBOL_ELLIPSIS if line_start > 0 else "")
                    + line[line_start:line_end]
                    + (SYMBOL_ELLIPSIS if line_end < len(line) else "")
                ]
            ]
            # include an indicator in the diff if this was not the last line
            + ([symbol_hidden_line] if line_idx_to < len(lines) else [])
        )

    return ndiff(adjust_lines(lines_a), adjust_lines(lines_b))
