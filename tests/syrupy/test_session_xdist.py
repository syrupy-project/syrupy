"""Unit tests for the pytest-xdist worker/controller report merging."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from syrupy.data import Snapshot, SnapshotCollection
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.report import SnapshotReport
from syrupy.session import ItemStatus, SnapshotSession
from syrupy.utils import compress_json, decompress_json

LOCATION = str(Path("/tmp", "__snapshots__", "test_a.ambr"))


def _options(**overrides) -> SimpleNamespace:
    defaults = {
        "keyword": "",
        "file_or_dir": [],
        "pyargs": False,
        "snapshot_file_lock": False,
        "snapshot_file_lock_timeout": 60.0,
        "update_snapshots": False,
        "warn_unused_snapshots": False,
        "no_cleanup": False,
        "include_snapshot_details": False,
        "disable_unused_snapshots": False,
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def _session(workeroutput: dict | None = None) -> SnapshotSession:
    config = SimpleNamespace(option=_options(), rootpath=Path("/tmp"))
    if workeroutput is not None:
        config.workeroutput = workeroutput
    session = SnapshotSession(pytest_session=SimpleNamespace(config=config))
    session.report = SnapshotReport(
        base_dir=Path("/tmp"),
        collected_items=set(),
        selected_items={},
        options=config.option,
        assertions=[],
    )
    return session


def _collection(*names: str) -> SnapshotCollection:
    collection = SnapshotCollection(location=LOCATION)
    for name in names:
        collection.add(Snapshot(name=name))
    return collection


def test_collection_serialize_roundtrip():
    collection = SnapshotCollection(location=LOCATION)
    collection.add(Snapshot(name="test_a"))
    collection.add(Snapshot(name="test_b"))

    from syrupy.data import SnapshotCollections

    collections = SnapshotCollections()
    collections.add(collection)

    restored = SnapshotCollections()
    restored.merge_serialized(collections.serialize())

    assert restored.serialize() == {LOCATION: ["test_a", "test_b"]}


def test_worker_publishes_minimal_report(monkeypatch):
    monkeypatch.setenv("PYTEST_XDIST_WORKER", "gw0")
    worker = _session(workeroutput={})
    worker.report.used.update(_collection("test_a"))
    worker.report.discovered.update(_collection("test_a", "test_b"))
    worker.report._num_xfails = 2
    worker._selected_items = {"test_a.py::test_a": ItemStatus.PASSED}
    worker._extensions = {LOCATION: AmberSnapshotExtension()}

    class _Obj:
        __module__ = "test_a"
        __name__ = "test_a"

    class _Item:
        nodeid = "test_a.py::test_a"
        name = "test_a"
        path = Path("/tmp/test_a.py")
        obj = _Obj()

    worker._collected_items = {"test_a.py::test_a": _Item()}

    worker._publish_worker_report()

    payload = worker.pytest_session.config.workeroutput["syrupy_report"]
    assert isinstance(payload["collections"], bytes)
    collections = decompress_json(payload["collections"])
    assert collections["used"] == {LOCATION: ["test_a"]}
    assert payload["num_xfails"] == 2
    assert payload["selected"] == {"test_a.py::test_a": "passed"}
    assert payload["extensions"] == {
        LOCATION: "syrupy.extensions.amber.AmberSnapshotExtension"
    }
    # gw0 is the only worker that ships the collected items.
    assert isinstance(payload["collected"], bytes)
    collected = decompress_json(payload["collected"])
    assert collected[0]["nodeid"] == "test_a.py::test_a"


def test_worker_compresses_large_collection_report(monkeypatch):
    monkeypatch.setenv("PYTEST_XDIST_WORKER", "gw1")
    worker = _session(workeroutput={})
    assert worker.report is not None
    names = [f"test_large_snapshot[{index}].{index}" for index in range(20_000)]
    worker.report.discovered.update(_collection(*names))
    worker.report.matched.update(_collection(*names))
    worker.report.used.update(_collection(*names))

    worker._publish_worker_report()

    compressed = worker.pytest_session.config.workeroutput["syrupy_report"][
        "collections"
    ]
    uncompressed = json.dumps(
        {
            name: getattr(worker.report, name).serialize()
            for name in (
                "discovered",
                "created",
                "failed",
                "matched",
                "updated",
                "used",
            )
        },
        separators=(",", ":"),
    ).encode()
    assert isinstance(compressed, bytes)
    assert len(compressed) < len(uncompressed) // 5

    controller = _session()
    controller.add_worker_report(
        worker.pytest_session.config.workeroutput["syrupy_report"]
    )
    controller._merge_worker_reports()
    assert controller.report is not None
    assert len(next(iter(controller.report.discovered))) == len(names)


def test_worker_without_workeroutput_is_noop():
    # A non-xdist session has no workeroutput; publishing must be safe.
    worker = _session()
    worker._publish_worker_report()  # should not raise


def test_non_gw0_worker_omits_collected(monkeypatch):
    monkeypatch.setenv("PYTEST_XDIST_WORKER", "gw1")
    worker = _session(workeroutput={})
    worker._publish_worker_report()
    assert "collected" not in worker.pytest_session.config.workeroutput["syrupy_report"]


def test_controller_uses_first_collected_only():
    controller = _session()
    first = {
        "nodeid": "test_a.py::test_a",
        "name": "test_a",
        "path": "/tmp/test_a.py",
        "modulename": "test_a",
        "methodname": "test_a",
    }
    second = {
        "nodeid": "test_b.py::test_b",
        "name": "test_b",
        "path": "/tmp/test_b.py",
        "modulename": "test_b",
        "methodname": "test_b",
    }
    empty_collections = {
        name: {}
        for name in (
            "discovered",
            "created",
            "failed",
            "matched",
            "updated",
            "used",
        )
    }
    controller.add_worker_report(
        {
            "collections": empty_collections,
            "num_xfails": 0,
            "selected": {},
            "extensions": {},
            "collected": compress_json([first]),
        }
    )
    controller.add_worker_report(
        {
            "collections": empty_collections,
            "num_xfails": 0,
            "selected": {},
            "extensions": {},
            "collected": compress_json([second]),
        }
    )
    controller._merge_worker_reports()
    items = {item.nodeid for item in controller.report.collected_items}
    assert items == {"test_a.py::test_a"}


def test_worker_publishes_write_sidecars(tmp_path: Path):
    worker = _session(workeroutput={})
    location = str(tmp_path / "snap.ambr")
    worker._written_snapshot_locations.add(location)
    worker._publish_write_sidecars()
    assert worker.pytest_session.config.workeroutput["syrupy_write_sidecars"] == [
        location
    ]


def test_controller_cleans_write_sidecars(tmp_path: Path):
    location = tmp_path / "snap.ambr"
    location.write_text("data", encoding="utf-8")
    lock_path = Path(str(location) + ".lock")
    tmp_sidecar = Path(str(location) + ".tmp")
    lock_path.write_text("", encoding="utf-8")
    tmp_sidecar.write_text("", encoding="utf-8")

    controller = _session()
    controller.add_written_snapshot_locations([str(location)])
    controller._cleanup_write_sidecars()

    assert location.exists()
    assert not lock_path.exists()
    assert not tmp_sidecar.exists()
    assert controller._written_snapshot_locations == set()


def test_remove_unused_tracks_locations_for_sidecar_cleanup(tmp_path: Path):
    """Unused deletion under --snapshot-file-lock must be included in cleanup."""
    from syrupy.data import SnapshotCollections
    from syrupy.extensions.amber.serializer import AmberDataSerializer
    from syrupy.utils import set_snapshot_file_lock

    location = tmp_path / "snap.ambr"
    seed = SnapshotCollection(location=str(location))
    seed.add(Snapshot(name="gone", data="'x'"))
    AmberDataSerializer.write_file(seed, merge=False, file_lock=False)

    controller = _session()
    controller.pytest_session.config.option = _options(snapshot_file_lock=True)
    set_snapshot_file_lock(True)
    try:
        controller._extensions[str(location)] = AmberSnapshotExtension()
        unused = SnapshotCollections()
        unused_collection = SnapshotCollection(location=str(location))
        unused_collection.add(Snapshot(name="gone", data="'x'"))
        unused.add(unused_collection)
        used = SnapshotCollections()

        controller.remove_unused_snapshots(
            unused_snapshot_collections=unused,
            used_snapshot_collections=used,
        )

        assert str(location) in controller._written_snapshot_locations
        lock_path = Path(str(location) + ".lock")
        # Lock may exist after delete; cleanup must clear it.
        controller._cleanup_write_sidecars()
        assert not lock_path.exists()
        assert not location.exists()
    finally:
        set_snapshot_file_lock(False)


def test_ran_items_skips_selected_missing_from_collected():
    """Regression for Windows xdist: selected without collected must not KeyError."""
    report = SnapshotReport(
        base_dir=Path("/tmp"),
        collected_items=set(),
        selected_items={"test_race.py::test_many[0]": ItemStatus.PASSED},
        options=_options(),
        assertions=[],
    )
    assert list(report.ran_items) == []
    assert list(report.skipped_items) == []


def test_merge_warns_when_selected_missing_from_collected():
    controller = _session()
    empty_collections = {
        name: {}
        for name in (
            "discovered",
            "created",
            "failed",
            "matched",
            "updated",
            "used",
        )
    }
    controller.add_worker_report(
        {
            "collections": empty_collections,
            "num_xfails": 0,
            "selected": {"test_race.py::test_many[0]": "passed"},
            "extensions": {},
        }
    )
    with pytest.warns(UserWarning, match="missing from collected items"):
        controller._merge_worker_reports()
    assert list(controller.report.ran_items) == []


def test_flush_tracks_location_before_write_for_sidecar_cleanup(
    tmp_path: Path, monkeypatch
):
    """Lock sidecars are tracked even when the write raises (e.g. lock timeout)."""
    from syrupy.location import PyTestLocation
    from syrupy.utils import set_snapshot_file_lock

    controller = _session()
    controller.pytest_session.config.option = _options(snapshot_file_lock=True)
    set_snapshot_file_lock(True)
    try:

        class _Obj:
            __module__ = "t"
            __name__ = "t"

        class _Item:
            nodeid = "t.py::t"
            name = "t"
            path = tmp_path / "t.py"
            fspath = path
            obj = _Obj()

        (tmp_path / "t.py").write_text("def t():\n    pass\n", encoding="utf-8")
        loc = PyTestLocation(_Item())
        ext = AmberSnapshotExtension()
        controller.queue_snapshot_write(ext, loc, "'x'", 0)
        ext_key = next(iter(controller._queued_snapshot_writes))
        _, snapshot_location = ext_key

        def _boom(*, snapshot_location, snapshots, name_order=None):
            raise TimeoutError("lock timeout")

        monkeypatch.setattr(AmberSnapshotExtension, "write_snapshot", _boom)
        with pytest.raises(TimeoutError, match="lock timeout"):
            controller.flush_snapshot_write_queue()
        assert snapshot_location in controller._written_snapshot_locations
    finally:
        set_snapshot_file_lock(False)


def test_controller_merges_worker_reports():
    controller = _session()
    controller.add_worker_report(
        {
            "collections": {
                "discovered": {LOCATION: ["test_a", "test_b"]},
                "created": {},
                "failed": {},
                "matched": {LOCATION: ["test_a"]},
                "updated": {},
                "used": {LOCATION: ["test_a"]},
            },
            "num_xfails": 1,
            "selected": {"test_a.py::test_a": "passed"},
            "extensions": {LOCATION: "syrupy.extensions.amber.AmberSnapshotExtension"},
            "collected": [
                {
                    "nodeid": "test_a.py::test_a",
                    "name": "test_a",
                    "path": "/tmp/test_a.py",
                    "modulename": "test_a",
                    "methodname": "test_a",
                }
            ],
        }
    )
    controller.add_worker_report(
        {
            "collections": {
                "discovered": {},
                "created": {},
                "failed": {},
                "matched": {},
                "updated": {},
                "used": {},
            },
            "num_xfails": 2,
            "selected": {"test_a.py::test_a": False},
            "extensions": {},
        }
    )

    controller._merge_worker_reports()

    report = controller.report
    assert report.used.serialize() == {LOCATION: ["test_a"]}
    assert report.discovered.serialize() == {LOCATION: ["test_a", "test_b"]}
    # xfail counts accumulate across workers.
    assert report._num_xfails == 3
    # The concrete PASSED status wins over NOT_RUN from the other worker.
    assert report.selected_items["test_a.py::test_a"] == ItemStatus.PASSED
    # Extension reconstructed for partial removal.
    assert isinstance(controller._extensions[LOCATION], AmberSnapshotExtension)
    # Collected item reconstructed for location matching.
    item = next(iter(report.collected_items))
    assert item.nodeid == "test_a.py::test_a"
    assert item.obj.__module__ == "test_a"


def test_controller_ignores_unimportable_extension():
    controller = _session()
    controller.add_worker_report(
        {
            "collections": {
                name: {}
                for name in (
                    "discovered",
                    "created",
                    "failed",
                    "matched",
                    "updated",
                    "used",
                )
            },
            "num_xfails": 0,
            "selected": {},
            "extensions": {LOCATION: "does.not.Exist"},
        }
    )
    controller._merge_worker_reports()
    assert LOCATION not in controller._extensions


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__])
