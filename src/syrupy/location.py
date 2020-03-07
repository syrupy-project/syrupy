from pathlib import Path
from typing import (
    Any,
    Optional,
)


class TestLocation:
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

    @property
    def snapshot_name(self) -> str:
        if self.classname is not None:
            return f"{self.classname}.{self.testname}"
        return str(self.testname)

    def __valid_id(self, name: str) -> str:
        [valid_id, *rest] = name
        while rest:
            new_valid_id = f"{valid_id}{rest.pop(0)}"
            if not new_valid_id.isidentifier():
                break
            valid_id = new_valid_id
        return valid_id

    def matches_snapshot_name(self, snapshot_name: str) -> bool:
        return self.__valid_id(self.snapshot_name) == self.__valid_id(snapshot_name)

    def matches_snapshot_location(self, snapshot_location: str) -> bool:
        return self.filename in snapshot_location
