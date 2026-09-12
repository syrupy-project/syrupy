"""Concurrent merge writes to a shared amber file (#1237)."""

from __future__ import annotations

import multiprocessing as mp
from pathlib import Path

import pytest

from syrupy.constants import TEXT_ENCODING
from syrupy.data import Snapshot, SnapshotCollection
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.extensions.amber.serializer import AmberDataSerializer
from syrupy.utils import (
    cleanup_snapshot_write_sidecars,
    set_snapshot_file_lock,
    snapshot_write_sidecar_paths,
)


@pytest.fixture(autouse=True)
def _enable_snapshot_file_lock():
    set_snapshot_file_lock(True)
    yield
    set_snapshot_file_lock(False)


def _seed_file(path: Path, count: int) -> None:
    collection = SnapshotCollection(location=str(path))
    for i in range(count):
        collection.add(Snapshot(name=f"snap[{i}]", data=f"'v1-{i}'"))
    # Explicit file_lock=False so seeding never creates sidecars.
    AmberDataSerializer.write_file(collection, merge=False, file_lock=False)


def _write_collection(
    filepath: str,
    snapshot_collection: SnapshotCollection,
    name_order: dict[str, int] | None = None,
) -> None:
    """Write amber bytes without locking (pre-#1237 behaviour)."""
    with open(filepath, "w", encoding=TEXT_ENCODING, newline=None) as f:
        f.write(
            f"{AmberDataSerializer._marker_prefix}"
            f"{AmberDataSerializer.Marker.Version}: "
            f"{AmberDataSerializer.VERSION}\n"
        )
        for snapshot in sorted(
            snapshot_collection,
            key=lambda s: AmberDataSerializer.snapshot_sort_key(s, name_order),
        ):
            snapshot_data = str(snapshot.data)
            if snapshot_data is None:
                continue
            f.write(
                f"{AmberDataSerializer._marker_prefix}"
                f"{AmberDataSerializer.Marker.Name}: {snapshot.name}\n"
            )
            parts = snapshot_data.split("\n")
            for i, part in enumerate(parts):
                is_last = i == len(parts) - 1
                if not is_last:
                    f.write(AmberDataSerializer.with_indent(part + "\n", 1))
                elif part:
                    f.write(AmberDataSerializer.with_indent(part, 1))
            if snapshot_data.endswith("\n"):
                f.write(AmberDataSerializer.with_indent("", 1))
            f.write(
                f"\n{AmberDataSerializer._marker_prefix}"
                f"{AmberDataSerializer.Marker.Divider}\n"
            )


def _unlocked_merge_range(
    path: str, start: int, stop: int, barrier: mp.Barrier
) -> None:
    """
    Unsynchronized RMW with a barrier after the read so every worker starts from
    the same base — the classic lost-update race from #1237.
    """
    base = AmberDataSerializer.read_file(path)
    barrier.wait(timeout=30)
    for i in range(start, stop):
        base.add(Snapshot(name=f"snap[{i}]", data=f"'v2-{i}'"))
    _write_collection(path, base)


def _locked_merge_range(path: str, start: int, stop: int) -> None:
    collection = SnapshotCollection(location=path)
    for i in range(start, stop):
        collection.add(Snapshot(name=f"snap[{i}]", data=f"'v2-{i}'"))
    # Pass file_lock explicitly — ContextVar does not cross spawn boundaries.
    AmberDataSerializer.write_file(collection, merge=True, file_lock=True)


def test_unsynchronized_merge_loses_snapshots(tmp_path: Path) -> None:
    """Without a lock, concurrent merges of disjoint slices lose updates."""
    count = 80
    workers = 8
    path = tmp_path / "shared.ambr"
    _seed_file(path, count)

    chunk = count // workers
    ctx = mp.get_context("spawn")
    barrier = ctx.Barrier(workers)
    procs = [
        ctx.Process(
            target=_unlocked_merge_range,
            args=(
                str(path),
                i * chunk,
                (i + 1) * chunk if i < workers - 1 else count,
                barrier,
            ),
        )
        for i in range(workers)
    ]
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join(timeout=30)
        assert proc.exitcode == 0

    result = AmberDataSerializer.read_file(str(path))
    updated = sum(
        1
        for i in range(count)
        if (snap := result.get(f"snap[{i}]")) is not None and snap.data == f"'v2-{i}'"
    )
    # Only one worker's slice can survive a barrier-synchronized lost update.
    assert updated < count
    assert len({snapshot.name for snapshot in result}) == count


def test_write_file_merge_preserves_all_snapshots_under_concurrency(
    tmp_path: Path,
) -> None:
    """AmberDataSerializer.write_file(merge=True) is safe across processes."""
    count = 80
    workers = 8
    path = tmp_path / "shared.ambr"
    _seed_file(path, count)

    chunk = count // workers
    ctx = mp.get_context("spawn")
    procs = [
        ctx.Process(
            target=_locked_merge_range,
            args=(
                str(path),
                i * chunk,
                (i + 1) * chunk if i < workers - 1 else count,
            ),
        )
        for i in range(workers)
    ]
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join(timeout=30)
        assert proc.exitcode == 0

    result = AmberDataSerializer.read_file(str(path))
    names = {snapshot.name for snapshot in result}
    assert names == {f"snap[{i}]" for i in range(count)}
    for i in range(count):
        snapshot = result.get(f"snap[{i}]")
        assert snapshot is not None
        assert snapshot.data == f"'v2-{i}'"

    cleanup_snapshot_write_sidecars(path)
    lock_path, tmp_sidecar = snapshot_write_sidecar_paths(path)
    assert not lock_path.exists()
    assert not tmp_sidecar.exists()


def test_write_file_cleans_tmp_sidecar_on_success(tmp_path: Path) -> None:
    path = tmp_path / "one.ambr"
    _seed_file(path, 1)
    collection = SnapshotCollection(location=str(path))
    collection.add(Snapshot(name="snap[0]", data="'v2-0'"))
    AmberDataSerializer.write_file(collection, merge=True, file_lock=True)

    lock_path, tmp_path_sidecar = snapshot_write_sidecar_paths(path)
    assert not tmp_path_sidecar.exists()
    # Lock may remain until session cleanup when write_file is used directly.
    assert lock_path.exists()
    cleanup_snapshot_write_sidecars(path)
    assert not lock_path.exists()


def test_write_file_without_file_lock_creates_no_sidecars(tmp_path: Path) -> None:
    path = tmp_path / "one.ambr"
    collection = SnapshotCollection(location=str(path))
    collection.add(Snapshot(name="snap[0]", data="'v1-0'"))
    AmberDataSerializer.write_file(collection, merge=False, file_lock=False)

    lock_path, tmp_sidecar = snapshot_write_sidecar_paths(path)
    assert path.exists()
    assert not lock_path.exists()
    assert not tmp_sidecar.exists()


def test_delete_snapshots_under_lock_preserves_remaining(tmp_path: Path) -> None:
    path = tmp_path / "shared.ambr"
    _seed_file(path, 3)
    AmberSnapshotExtension().delete_snapshots(str(path), {"snap[1]"})

    result = AmberDataSerializer.read_file(str(path))
    assert {snapshot.name for snapshot in result} == {"snap[0]", "snap[2]"}
    assert result.get("snap[0]") is not None
    assert result.get("snap[0]").data == "'v1-0'"


def test_delete_snapshots_under_lock_unlinks_when_empty(tmp_path: Path) -> None:
    path = tmp_path / "one.ambr"
    _seed_file(path, 1)
    AmberSnapshotExtension().delete_snapshots(str(path), {"snap[0]"})
    assert not path.exists()
