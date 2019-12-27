import inspect
from typing import (
    Any,
    Optional,
    Type,
)


class TestLocation(object):
    def __init__(self, node: Any):
        self._node = node
        self.filename = node.fspath
        self.nodename = getattr(node, "name", None)
        method = node.obj
        self.modulename = method.__module__
        self.methodname = method.__name__
        self.testname = self.nodename or self.methodname
        method_class = self.__get_method_class(method)
        self.classname = method_class.__name__ if method_class else None

    @staticmethod
    def __get_method_class(m: Any) -> Optional[Type[Any]]:
        if inspect.ismethod(m):
            for cls in inspect.getmro(m.__self__.__class__):
                if m.__name__ in cls.__dict__:
                    return cls
        return None

    def matches_snapshot_name(self, snapshot_name: str) -> bool:
        return self.methodname in snapshot_name or snapshot_name in self.nodename
