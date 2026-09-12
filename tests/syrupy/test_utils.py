from pathlib import Path

import pytest

from syrupy.exceptions import FailedToLoadModuleMember
from syrupy.utils import (
    compress_json,
    decompress_json,
    import_module_member,
    is_snapshot_write_sidecar,
    replace_atomic,
    walk_snapshot_dir,
)


def makefiles(testdir, filetree, root=""):
    for filename, contents in filetree.items():
        filepath = Path(root).joinpath(filename)
        if isinstance(contents, dict):
            testdir.mkdir(filepath)
            makefiles(testdir, contents, str(filepath))
        else:
            name, ext = str(filepath.with_name(filepath.stem)), filepath.suffix
            testdir.makefile(ext, **{name: contents})


@pytest.fixture
def testfiles(testdir):
    filetree = {
        "file1.txt": "file1",
        "file2.txt": "file2",
        "__snapshot__": {
            "wrong_snapfile1.ambr": "",
            "wrong_snapfolder": {"wrong_snapfile2.svg": "<svg></svg>"},
        },
        "__snapshots__": {
            "snapfile1.ambr": "",
            "snapfolder": {"snapfile2.svg": "<svg></svg>"},
        },
    }
    makefiles(testdir, filetree)
    return filetree, testdir


def test_walk_dir_skips_non_snapshot_path(testfiles):
    _, testdir = testfiles
    snap_folder = Path("__snapshots__")
    assert {
        str(Path(p).relative_to(Path.cwd()))
        for p in walk_snapshot_dir(Path(testdir.tmpdir).joinpath(snap_folder))
    } == {
        str(snap_folder.joinpath("snapfile1.ambr")),
        str(snap_folder.joinpath("snapfolder", "snapfile2.svg")),
    }


def test_walk_dir_ignores_ignored_extensions(testdir):
    filetree = {
        "file1.txt": "file1",
        "file2.txt": "file2",
        "__snapshots__": {
            "snapfile1.ambr": "",
            "snapfile1.ambr.dvc": "",
            "snapfolder": {"snapfile2.svg": "<svg></svg>"},
        },
    }
    makefiles(testdir, filetree)

    discovered_files = {
        str(Path(p).relative_to(Path.cwd()))
        for p in walk_snapshot_dir(
            Path(testdir.tmpdir).joinpath("__snapshots__"), ignore_extensions=["dvc"]
        )
    }

    assert discovered_files == {
        str(Path("__snapshots__").joinpath("snapfile1.ambr")),
        str(Path("__snapshots__").joinpath("snapfolder", "snapfile2.svg")),
    }

    assert (
        str(Path("__snapshots__").joinpath("snapfile1.ambr.dvc"))
        not in discovered_files
    )


def test_walk_dir_skips_write_sidecars(testdir):
    snap_dir = Path(testdir.tmpdir).joinpath("__snapshots__")
    snap_dir.mkdir()
    (snap_dir / "snapfile1.ambr").write_text("")
    (snap_dir / "snapfile1.ambr.lock").write_text("")
    (snap_dir / "snapfile1.ambr.tmp").write_text("")
    (snap_dir / "photo.tmp").write_text("")
    (snap_dir / "data.lock").write_text("")

    discovered_files = {
        str(Path(p).relative_to(Path(testdir.tmpdir)))
        for p in walk_snapshot_dir(snap_dir)
    }

    assert discovered_files == {
        str(Path("__snapshots__").joinpath("snapfile1.ambr")),
        str(Path("__snapshots__").joinpath("photo.tmp")),
        str(Path("__snapshots__").joinpath("data.lock")),
    }


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("snap.ambr.lock", True),
        ("snap.ambr.tmp", True),
        ("photo.tmp", False),
        ("data.lock", False),
        ("snap.ambr", False),
    ],
)
def test_is_snapshot_write_sidecar(name: str, expected: bool) -> None:
    assert is_snapshot_write_sidecar(name) is expected


def test_replace_atomic_retries_permission_error(tmp_path: Path, monkeypatch) -> None:
    src = tmp_path / "file.tmp"
    dst = tmp_path / "file"
    src.write_text("new", encoding="utf-8")
    dst.write_text("old", encoding="utf-8")

    calls = {"n": 0}
    real_replace = __import__("os").replace

    def flaky(source, destination):
        calls["n"] += 1
        if calls["n"] < 3:
            raise PermissionError("busy")
        real_replace(source, destination)

    monkeypatch.setattr("syrupy.utils.os.replace", flaky)
    monkeypatch.setattr("syrupy.utils.time.sleep", lambda _seconds: None)

    replace_atomic(src, dst)
    assert dst.read_text(encoding="utf-8") == "new"
    assert calls["n"] == 3


def test_replace_atomic_raises_after_exhausted_retries(
    tmp_path: Path, monkeypatch
) -> None:
    src = tmp_path / "file.tmp"
    dst = tmp_path / "file"
    src.write_text("new", encoding="utf-8")
    dst.write_text("old", encoding="utf-8")

    monkeypatch.setattr(
        "syrupy.utils.os.replace",
        lambda _src, _dst: (_ for _ in ()).throw(PermissionError("busy")),
    )
    monkeypatch.setattr("syrupy.utils.time.sleep", lambda _seconds: None)

    with pytest.raises(OSError, match="after retries"):
        replace_atomic(src, dst)


def test_compress_json_roundtrip() -> None:
    payload = {"used": {"/tmp/a.ambr": ["test_a"]}, "n": 2}
    encoded = compress_json(payload)
    assert isinstance(encoded, bytes)
    assert decompress_json(encoded) == payload


def dummy_member():
    return 123


def test_import_module_member_imports_member():
    imported_member = import_module_member(f"{__name__}.dummy_member")
    assert imported_member() == 123


@pytest.mark.parametrize(
    "path",
    [
        "dummy_member",
        f"{__name__}badpath.dummy_member",
        f"{__name__}.dummy_memberbadmember",
    ],
)
def test_import_module_member_with_bad_path_raises_exception(path):
    with pytest.raises(FailedToLoadModuleMember):
        import_module_member(path)
