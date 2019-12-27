import inspect
from typing import (
    Any,
    Optional,
)


class TestLocation(object):
    def __init__(self, node: Any):
        self._node = node
        self.filename = self._node.fspath
        self.modulename = self._node.obj.__module__
        self.methodname = self._node.obj.__name__
        self.nodename = getattr(self._node, "name", None)
        self.testname = self.nodename or self.methodname

    @property
    def classname(self) -> Optional[str]:
        if inspect.ismethod(self._node.obj):
            method = self._node.obj
            for cls in inspect.getmro(method.__self__.__class__):
                if method.__name__ in cls.__dict__:
                    return cls.__name__
        return None

    def matches_snapshot_name(self, snapshot_name: str) -> bool:
        matches_basemethod = str(self.methodname) in snapshot_name
        matches_testnode = snapshot_name in str(self.nodename)
        return matches_basemethod or matches_testnode
