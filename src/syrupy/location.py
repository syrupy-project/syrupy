from collections.abc import Iterator
from dataclasses import (
    dataclass,
    field,
)
from pathlib import Path

import pytest

from syrupy.constants import PYTEST_NODE_SEP
from syrupy.extensions.base import SnapshotCollectionStorage


@dataclass(frozen=True)
class PyTestLocation:
    item: "pytest.Item"
    nodename: str | None = field(init=False)
    testname: str = field(init=False)
    methodname: str = field(init=False)
    modulename: str = field(init=False)
    filepath: str = field(init=False)

    def __post_init__(self) -> None:
        # NB. we're in a frozen dataclass, but need to transform the values that the caller
        # supplied... we do so by (ab)using object.__setattr__ to forcibly set the attributes. (See
        # rejected PEP-0712 for an example of a better way to handle this.)
        #
        # This is safe because this all happens during initialization: `self` hasn't been hashed
        # (or, e.g., stored in a dict), so the mutation won't be noticed.
        if self.is_doctest:
            return self.__attrs_post_init_doc__()
        self.__attrs_post_init_def__()

    def __attrs_post_init_def__(self) -> None:
        node_path: Path = getattr(self.item, "path")  # noqa: B009
        # See __post_init__ for discussion of object.__setattr__
        object.__setattr__(self, "filepath", str(node_path.absolute()))
        obj = getattr(self.item, "obj")  # noqa: B009
        object.__setattr__(self, "modulename", obj.__module__)
        object.__setattr__(self, "methodname", obj.__name__)
        object.__setattr__(self, "nodename", getattr(self.item, "name", None))
        object.__setattr__(self, "testname", self.nodename or self.methodname)

    def __attrs_post_init_doc__(self) -> None:
        doctest = getattr(self.item, "dtest")  # noqa: B009
        # See __post_init__ for discussion of object.__setattr__
        object.__setattr__(self, "filepath", doctest.filename)
        test_relfile, test_node = self.nodeid.split(PYTEST_NODE_SEP)
        test_relpath = Path(test_relfile)
        object.__setattr__(
            self,
            "modulename",
            ".".join([*test_relpath.parent.parts, test_relpath.stem]),
        )
        object.__setattr__(self, "methodname", None)
        object.__setattr__(
            self, "nodename", test_node.replace(f"{self.modulename}.", "")
        )
        object.__setattr__(self, "testname", self.nodename or self.methodname)

    @property
    def is_item_parametrized(self) -> bool:
        return self.nodeid.endswith("]")

    @property
    def classname(self) -> str | None:
        if self.is_doctest:
            return None
        return ".".join(self.nodeid.split(PYTEST_NODE_SEP)[1:-1]) or None

    @property
    def nodeid(self) -> str:
        """
        Pytest node names contain file path and module members delimited by `::`

        Examples:
        - tests/grouping/test_file.py::TestClass::TestSubClass::test_method
        - tests/grouping/test_file.py::DocTestClass.doc_test_method
        - tests/grouping/test_file.py::doctestfile.txt

        :raises: `AttributeError` if node has no node id
        :return: test node id
        """
        return str(getattr(self.item, "nodeid"))  # noqa: B009

    @property
    def basename(self) -> str:
        return Path(self.filepath).stem

    @property
    def snapshot_name(self) -> str:
        if self.classname is not None:
            return f"{self.classname}.{self.testname}"
        return str(self.testname)

    @property
    def snapshot_name_parametrized(self) -> str:
        if self.classname is not None:
            return f"{self.classname}.{self.nodename}"
        return str(self.nodename)

    @property
    def is_doctest(self) -> bool:
        return self.__is_doctest(self.item)

    def __is_doctest(self, node: "pytest.Item") -> bool:
        return hasattr(node, "dtest")

    def __valid_id(self, name: str) -> str:
        """
        Take characters from the name while the result would be a valid python
        identified. Example: "test_2[A]" returns "test_2" while "1_a" would return ""
        """
        valid_id = ""
        for char in name:
            new_valid_id = f"{valid_id}{char}"
            if not new_valid_id.isidentifier():
                break
            valid_id = new_valid_id
        return valid_id

    def __valid_ids(self, name: str) -> Iterator[str]:
        """
        Break a name path into valid name parts stopping at the first non valid name.
        Example "TestClass.test_method_[1]" would yield ("TestClass", "test_method_")
        """
        for n in name.split("."):
            valid_id = self.__valid_id(n)
            if valid_id:
                yield valid_id
            if valid_id != n:
                break

    def __parse(self, name: str) -> str:
        return ".".join(self.__valid_ids(name))

    def matches_snapshot_name(self, snapshot_name: str) -> bool:
        return self.__parse(self.snapshot_name) == self.__parse(snapshot_name)

    def matches_snapshot_location(self, snapshot_location: str) -> bool:
        loc = Path(snapshot_location)
        if not self._matches_snapshot_basename(loc):
            return False
        return self._matches_test_site(loc)

    def _matches_snapshot_basename(self, loc: Path) -> bool:
        # "test_file" should match "test_file.ext" or "test_file/whatever.ext", but not
        # "test_file_suffix.ext" (see PR #607).
        if self.basename == loc.stem:
            return True
        if self.basename != loc.parent.name:
            return False
        if not self.is_item_parametrized:
            return True
        # Parametrized single-file snapshots (see PR #965).
        return (
            loc.stem == self.snapshot_name_parametrized
            or loc.stem.startswith(f"{self.snapshot_name_parametrized}.")
            or loc.stem.startswith(f"{self.snapshot_name_parametrized}[")
        )

    def _matches_test_site(self, loc: Path) -> bool:
        """
        Ensure a snapshot path belongs to this test file's site.

        Basename-only matching is not enough: ``test_views`` in one module must
        not match ``__snapshots__/test_views`` from another module's directory.
        """
        test_dir = Path(self.filepath).parent.resolve()
        resolved = loc.resolve()

        try:
            resolved.relative_to(test_dir)
            return True
        except ValueError:
            pass

        snapshot_test_dir = self._snapshot_collection_test_dir(resolved)
        if snapshot_test_dir is not None:
            # Snapshot is in a collection directory (e.g. ``__snapshots__/``); only
            # the test files alongside that directory may claim it.
            return snapshot_test_dir == test_dir

        # Snapshots stored outside the test file directory (custom dirname locations).
        return True

    @staticmethod
    def _snapshot_collection_test_dir(loc: Path) -> Path | None:
        """
        Return the test directory that owns a snapshot collection path.

        Walks upward from ``loc`` looking for a snapshot collection directory
        (``__snapshots__`` by default, or ``--snapshot-dirname``). There is no
        fixed depth limit: any ancestor may be the collection dir, and snapshots
        may be nested arbitrarily deep beneath it (e.g. single-file extension
        layouts). When found, snapshots belong to the collection dir's parent.
        """
        for parent in loc.parents:
            if PyTestLocation._is_snapshot_dir(parent):
                return parent.parent.resolve()
        return None

    @staticmethod
    def _is_snapshot_dir(path: Path) -> bool:
        return path.name == str(SnapshotCollectionStorage.snapshot_dirname)
