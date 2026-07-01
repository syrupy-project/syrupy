"""Unit tests for the pytest-xdist worker/controller report merging."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from syrupy.data import Snapshot, SnapshotCollection
from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.report import SnapshotReport
from syrupy.session import ItemStatus, SnapshotSession

LOCATION = str(Path("/tmp", "__snapshots__", "test_a.ambr"))


def _options() -> SimpleNamespace:
    return SimpleNamespace(keyword="", file_or_dir=[], pyargs=False)


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

    worker._collected_items = {_Item()}

    worker._publish_worker_report()

    payload = worker.pytest_session.config.workeroutput["syrupy_report"]
    assert payload["collections"]["used"] == {LOCATION: ["test_a"]}
    assert payload["num_xfails"] == 2
    assert payload["selected"] == {"test_a.py::test_a": "passed"}
    assert payload["extensions"] == {
        LOCATION: "syrupy.extensions.amber.AmberSnapshotExtension"
    }
    # gw0 is the only worker that ships the collected items.
    assert payload["collected"][0]["nodeid"] == "test_a.py::test_a"


def test_worker_without_workeroutput_is_noop():
    # A non-xdist session has no workeroutput; publishing must be safe.
    worker = _session()
    worker._publish_worker_report()  # should not raise


def test_non_gw0_worker_omits_collected(monkeypatch):
    monkeypatch.setenv("PYTEST_XDIST_WORKER", "gw1")
    worker = _session(workeroutput={})
    worker._publish_worker_report()
    assert "collected" not in worker.pytest_session.config.workeroutput["syrupy_report"]


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
