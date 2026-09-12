import json
import os
import time
import zlib
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from contextvars import ContextVar
from difflib import ndiff
from gettext import gettext
from importlib import import_module
from pathlib import Path
from typing import (
    Any,
)

from .constants import (
    DIFF_LINE_COUNT_LIMIT,
    DIFF_LINE_WIDTH_LIMIT,
    SYMBOL_ELLIPSIS,
)
from .exceptions import FailedToLoadModuleMember

# Set from SnapshotSession via config.option.snapshot_file_lock (see session.start/finish).
_snapshot_file_lock: ContextVar[bool] = ContextVar(
    "syrupy_snapshot_file_lock", default=False
)
_FILE_LOCK_TIMEOUT_SECONDS = 30.0


def is_xdist_worker() -> bool:
    worker_name = os.getenv("PYTEST_XDIST_WORKER")
    return bool(worker_name and worker_name != "master")


def is_xdist_gw0() -> bool:
    """True on the pytest-xdist worker named ``gw0`` (used for one-shot payloads)."""
    return os.getenv("PYTEST_XDIST_WORKER") == "gw0"


def compress_json(data: Any) -> bytes:
    """JSON-encode ``data`` and zlib-compress for xdist workeroutput payloads."""
    return zlib.compress(json.dumps(data, separators=(",", ":")).encode())


def decompress_json(data: bytes) -> Any:
    """Inverse of :func:`compress_json`."""
    return json.loads(zlib.decompress(data))


def set_snapshot_file_lock(enabled: bool) -> None:
    """
    Enable or disable amber write locking for this context.

    Prefer :class:`~syrupy.session.SnapshotSession`, which sets this from
    ``config.option.snapshot_file_lock``. Direct callers (tests, scripts) may
    set it explicitly or pass ``file_lock=`` into
    :meth:`~syrupy.extensions.amber.serializer.AmberDataSerializer.write_file`.
    """
    _snapshot_file_lock.set(enabled)


def snapshot_file_lock_enabled() -> bool:
    """Whether ``--snapshot-file-lock`` is active in this context."""
    return _snapshot_file_lock.get()


def snapshot_write_sidecar_paths(filepath: str | Path) -> tuple[Path, Path]:
    """Return ``(lock_path, tmp_path)`` sidecars for a snapshot file write."""
    path = Path(filepath)
    return path.with_name(path.name + ".lock"), Path(f"{path}.tmp")


def is_snapshot_write_sidecar(filepath: str | Path) -> bool:
    """
    True for write sidecars named ``{file.with.ext}.lock`` / ``.tmp``.

    Single-suffix names like ``photo.tmp`` are treated as real snapshot files.
    """
    name = Path(filepath).name
    for suffix in (".lock", ".tmp"):
        if name.endswith(suffix):
            base = name[: -len(suffix)]
            if "." in base:
                return True
    return False


def cleanup_snapshot_write_sidecars(*filepaths: str | Path) -> None:
    """Remove lock/tmp sidecars for the given snapshot file paths."""
    for filepath in filepaths:
        lock_path, tmp_path = snapshot_write_sidecar_paths(filepath)
        lock_path.unlink(missing_ok=True)
        tmp_path.unlink(missing_ok=True)


def replace_atomic(src: str | Path, dst: str | Path) -> None:
    """
    Replace ``dst`` with ``src`` (like ``os.replace``), with Windows retries.

    On Windows, ``os.replace`` can raise ``PermissionError`` if another process
    briefly has ``dst`` open; retry before surfacing a clear error.
    """
    src_path, dst_path = Path(src), Path(dst)
    last_error: OSError | None = None
    delays = (0.01, 0.02, 0.05, 0.1, 0.1, 0.2, 0.2, 0.5)
    for delay in delays:
        try:
            os.replace(src_path, dst_path)
            return
        except PermissionError as exc:
            last_error = exc
            time.sleep(delay)
        except OSError as exc:
            raise OSError(
                f"Failed to atomically replace '{dst_path}' with '{src_path}': {exc}"
            ) from exc
    raise OSError(
        f"Failed to atomically replace '{dst_path}' with '{src_path}' "
        f"after retries: {last_error}"
    ) from last_error


def _lock_timeout_error(path: Path) -> TimeoutError:
    return TimeoutError(
        f"Timed out after {_FILE_LOCK_TIMEOUT_SECONDS:.0f}s "
        f"waiting for exclusive lock on '{path}'"
    )


def _acquire_exclusive_lock(lock_file: Any, path: Path) -> None:
    """Block until an exclusive lock is acquired, or raise after the timeout."""
    deadline = time.monotonic() + _FILE_LOCK_TIMEOUT_SECONDS
    delay = 0.01
    if os.name == "nt":
        import msvcrt

        while True:
            try:
                lock_file.seek(0)
                if lock_file.read(1) != b"\0":
                    lock_file.seek(0)
                    lock_file.write(b"\0")
                    lock_file.flush()
                lock_file.seek(0)
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)  # type: ignore[attr-defined]
                return
            except OSError:
                if time.monotonic() >= deadline:
                    raise _lock_timeout_error(path) from None
                time.sleep(delay)
                delay = min(delay * 1.5, 0.1)
    else:
        import fcntl

        while True:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise _lock_timeout_error(path) from None
                time.sleep(delay)
                delay = min(delay * 1.5, 0.1)


def _release_exclusive_lock(lock_file: Any) -> None:
    if os.name == "nt":
        import msvcrt

        lock_file.seek(0)
        msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)  # type: ignore[attr-defined]
    else:
        import fcntl

        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


@contextmanager
def exclusive_file_lock(filepath: str | Path) -> Iterator[None]:
    """
    Cross-process exclusive lock for coordinating snapshot file updates.

    Used so pytest-xdist workers can safely read-modify-write the same amber
    file without silently clobbering each other's merges (see #1237).

    Waits up to 30s on both Unix and Windows, then raises ``TimeoutError``.

    Lockfiles are not deleted on release (unsafe with concurrent openers).
    :class:`~syrupy.session.SnapshotSession` removes them after the run when no
    writers remain (and on interrupt during ``finish``).
    """
    path = Path(filepath)
    lock_path, _ = snapshot_write_sidecar_paths(path)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+b") as lock_file:
        _acquire_exclusive_lock(lock_file, path)
        try:
            yield
        finally:
            _release_exclusive_lock(lock_file)


def walk_snapshot_dir(
    root: str | Path, *, ignore_extensions: list[str] | None = None
) -> Iterator[str]:
    ignore_exts: set[str] = set(ignore_extensions or [])

    for filepath in Path(root).rglob("*"):
        if not filepath.name.startswith(".") and filepath.is_file():
            # Sidecars from concurrent amber writes (#1237), e.g. ``a.ambr.lock``.
            if is_snapshot_write_sidecar(filepath):
                continue
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


def set_attrs(obj: Any, attrs: dict[str, Any]) -> Any:
    for k in attrs:
        setattr(obj, k, attrs[k])


@contextmanager
def obj_attrs(obj: Any, attrs: dict[str, Any]) -> Iterator[None]:
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
        line_a = "".join(lines_a[i : i + 1])
        line_b = "".join(lines_b[i : i + 1])
        if line_a != line_b:
            first_diff_line_idx = i
            for j in range(max(len(line_a), len(line_b))):
                char_a = line_a[j : j + 1]
                char_b = line_b[j : j + 1]
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
