from pathlib import Path
from typing import (
    Iterator,
    Optional,
)

import attr
import pytest

from syrupy.constants import PYTEST_NODE_SEP


@attr.s
class PyTestLocation:
    _node: "pytest.Item" = attr.ib()
    nodename: Optional[str] = attr.ib(init=False)
    testname: str = attr.ib(init=False)
    methodname: str = attr.ib(init=False)
    modulename: str = attr.ib(init=False)
    filepath: str = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self.filepath = getattr(self._node, "fspath")  # noqa: B009
        obj = getattr(self._node, "obj")  # noqa: B009
        self.modulename = obj.__module__
        self.methodname = obj.__name__
        self.nodename = getattr(self._node, "name", None)
        self.testname = self.nodename or self.methodname

    @property
    def classname(self) -> Optional[str]:
        """
        Pytest node names contain file path and module members delimited by `::`
        Example tests/grouping/test_file.py::TestClass::TestSubClass::test_method
        """
        nodeid: Optional[str] = getattr(self._node, "nodeid", None)
        if nodeid is None:
            return None
        return ".".join(nodeid.split(PYTEST_NODE_SEP)[1:-1]) or None

    @property
    def filename(self) -> str:
        return Path(self.filepath).stem

    @property
    def snapshot_name(self) -> str:
        if self.classname is not None:
            return f"{self.classname}.{self.testname}"
        return str(self.testname)

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
        return self.filename in snapshot_location
