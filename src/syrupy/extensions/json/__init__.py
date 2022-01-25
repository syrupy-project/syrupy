import datetime
import json
from gettext import gettext
from pathlib import Path
from types import GeneratorType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
)

from syrupy.constants import SYMBOL_ELLIPSIS
from syrupy.data import SnapshotFossil
from syrupy.extensions.amber.serializer import Repr
from syrupy.extensions.single_file import SingleFileSnapshotExtension

if TYPE_CHECKING:
    from syrupy.types import (
        PropertyFilter,
        PropertyMatcher,
        PropertyPath,
        SerializableData,
        SerializedData,
    )


class JSONSnapshotExtension(SingleFileSnapshotExtension):
    _max_depth: int = 99

    @property
    def _file_extension(self) -> str:
        return "json"

    @classmethod
    def sort(cls, iterable: Iterable[Any]) -> Iterable[Any]:
        try:
            return sorted(iterable)
        except TypeError:
            return sorted(iterable, key=str)

    @classmethod
    def __is_namedtuple(cls, obj: Any) -> bool:
        return isinstance(obj, tuple) and all(
            type(n) == str for n in getattr(obj, "_fields", [None])
        )

    @classmethod
    def _filter(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        path: "PropertyPath",
        exclude: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
        visited: Optional[Set[Any]] = None,
    ) -> "SerializableData":
        data_id = id(data)
        visited = set() if visited is None else visited
        if depth > cls._max_depth or data_id in visited:
            data = Repr(SYMBOL_ELLIPSIS)
        elif matcher:
            data = matcher(data=data, path=path)

        if isinstance(data, (int, float, str)):
            return data

        filtered_dct: Dict[Any, Any]
        if isinstance(data, (dict,)):
            filtered_dct = {}
            for key, value in data.items():
                if exclude and exclude(prop=key, path=path):
                    continue
                if not isinstance(key, (str,)):
                    continue
                filtered_dct[key] = cls._filter(
                    data=value,
                    depth=depth + 1,
                    path=(*path, (key, type(value))),
                    exclude=exclude,
                    matcher=matcher,
                    visited={*visited, data_id},
                )
            return filtered_dct

        if cls.__is_namedtuple(data):
            filtered_dct = {}
            for key in cls.sort(data._fields):
                value = getattr(data, key)
                filtered_dct[key] = cls._filter(
                    data=value,
                    depth=depth + 1,
                    path=(*path, (key, type(value))),
                    exclude=exclude,
                    matcher=matcher,
                    visited={*visited, data_id},
                )
            return filtered_dct

        if isinstance(data, (set, frozenset, list, tuple, GeneratorType)):
            filtered_lst: List[Any] = []
            iterable = (
                cls.sort(data) if isinstance(data, (set, frozenset)) else list(data)
            )
            for key, value in enumerate(iterable):
                filtered_lst.append(
                    cls._filter(
                        data=value,
                        depth=depth + 1,
                        path=(*path, (key, type(value))),
                        exclude=exclude,
                        matcher=matcher,
                        visited={*visited, data_id},
                    )
                )
            return filtered_lst

        if isinstance(data, (datetime.datetime,)):
            return data.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

        if data.__class__.__repr__ != object.__repr__:
            return repr(data)

        return f"<class '{data.__class__.__name__}'>"

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> "SerializedData":
        data = self._filter(
            data=data, depth=0, path=(), exclude=exclude, matcher=matcher
        )
        return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"

    def _read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str
    ) -> Optional["SerializableData"]:
        try:
            return Path(snapshot_location).read_text(encoding="utf-8")
        except FileNotFoundError:
            return None

    def _write_snapshot_fossil(self, *, snapshot_fossil: SnapshotFossil) -> None:
        filepath, data = snapshot_fossil.location, next(iter(snapshot_fossil)).data
        if not isinstance(data, str):
            error_text = gettext("Can't write into a file. Expected '{}', got '{}'")
            raise TypeError(error_text.format(str.__name__, type(data).__name__))
        Path(filepath).write_text(data, encoding="utf-8")
