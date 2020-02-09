import os
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
        return str(os.path.splitext(os.path.basename(self.filepath))[0])

    def matches_snapshot_name(self, snapshot_name: str) -> bool:
        matches_basemethod = str(self.methodname) in snapshot_name
        matches_testnode = snapshot_name in str(self.nodename)
        return matches_basemethod or matches_testnode

    def matches_snapshot_location(self, snapshot_location: str) -> bool:
        return self.filename in snapshot_location
