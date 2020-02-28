from pathlib import Path
from typing import (
    Any,
    Optional,
)


class TestLocation(object):
    def __init__(self, node: Any):
        self._node = node
        self.filepath = self._node.fspath
        self.modulename = self._node.obj.__module__
        self.methodname = self._node.obj.__name__
        self.nodename = getattr(self._node, "name", None)
        self.testname = self.nodename or self.methodname

    @property
    def classname(self) -> Optional[str]:
        classes = self._node.obj.__qualname__.split(".")[:-1]
        return ".".join(classes) if classes else None

    @property
    def filename(self) -> str:
        return Path(self.filepath).stem

    def __matches_snapshot_name(self, var_name: str, snapshot_name: str) -> bool:
        if var_name.isidentifier():
            return var_name in snapshot_name
        return snapshot_name in var_name

    def matches_snapshot_name(self, snapshot_name: str) -> bool:
        return self.__matches_snapshot_name(
            str(self.methodname), snapshot_name
        ) or self.__matches_snapshot_name(str(self.nodename), snapshot_name)

    def matches_snapshot_location(self, snapshot_location: str) -> bool:
        return self.filename in snapshot_location
