from dataclasses import (
    dataclass,
    field,
)
from pathlib import Path
from typing import (
    Iterator,
    Optional,
)

import pytest

from syrupy.constants import PYTEST_NODE_SEP


@dataclass
class PyTestLocation:
    item: "pytest.Item"
    nodename: Optional[str] = field(init=False)
    testname: str = field(init=False)
    methodname: str = field(init=False)
    modulename: str = field(init=False)
    filepath: str = field(init=False)

    def __post_init__(self) -> None:
        if self.is_doctest:
            return self.__attrs_post_init_doc__()
        self.__attrs_post_init_def__()

    def __attrs_post_init_def__(self) -> None:
        node_path: Path = getattr(self.item, "path")  # noqa: B009
        self.filepath = str(node_path.absolute())
        obj = getattr(self.item, "obj")  # noqa: B009
        self.modulename = obj.__module__
        self.methodname = obj.__name__
        self.nodename = getattr(self.item, "name", None)
        self.testname = self.nodename or self.methodname

    def __attrs_post_init_doc__(self) -> None:
        doctest = getattr(self.item, "dtest")  # noqa: B009
        self.filepath = doctest.filename
        test_relfile, test_node = self.nodeid.split(PYTEST_NODE_SEP)
        test_relpath = Path(test_relfile)
        self.modulename = ".".join([*test_relpath.parent.parts, test_relpath.stem])
        self.nodename = test_node.replace(f"{self.modulename}.", "")
        self.testname = self.nodename or self.methodname

    @property
    def classname(self) -> Optional[str]:
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
        # "test_file" should match_"test_file.ext" or "test_file/whatever.ext", but not
        # "test_file_suffix.ext"
        return self.basename == loc.stem or self.basename == loc.parent.name
