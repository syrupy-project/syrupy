from pathlib import Path

import pytest

from syrupy.exceptions import FailedToLoadModuleMember
from syrupy.utils import (
    import_module_member,
    walk_snapshot_dir,
)


def makefiles(testdir, filetree, root=""):
    for filename, contents in filetree.items():
        filepath = Path(root).joinpath(filename)
        if isinstance(contents, dict):
            testdir.mkdir(filepath)
            makefiles(testdir, contents, filepath)
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
    assert {
        str(Path(p).relative_to(Path.cwd())) for p in walk_snapshot_dir(testdir.tmpdir)
    } == {"__snapshots__/snapfile1.ambr", "__snapshots__/snapfolder/snapfile2.svg"}


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
