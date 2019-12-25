import os

import pytest

from syrupy.utils import walk_snapshot_dir


def makefiles(testdir, filetree, root=""):
    for filename, contents in filetree.items():
        filepath = os.path.join(root, filename)
        if isinstance(contents, dict):
            testdir.mkdir(filepath)
            makefiles(testdir, contents, filepath)
        else:
            name, ext = os.path.splitext(filepath)
            testdir.makefile(ext, **{name: contents})


@pytest.fixture
def testfiles(testdir):
    filetree = {
        "file1.txt": "file1",
        "file2.txt": "file2",
        "__snapshot__": {
            "wrong_snapfile1.yaml": "",
            "wrong_snapfolder": {"wrong_snapfile2.svg": "<svg></svg>"},
        },
        "__snapshots__": {
            "snapfile1.yaml": "",
            "snapfolder": {"snapfile2.svg": "<svg></svg>"},
        },
    }
    makefiles(testdir, filetree)
    return filetree, testdir


def test_walk_dir_skips_non_snapshot_path(testfiles):
    _, testdir = testfiles
    assert {os.path.relpath(p) for p in walk_snapshot_dir(testdir.tmpdir)} == {
        "__snapshots__/snapfile1.yaml",
        "__snapshots__/snapfolder/snapfile2.svg",
    }
