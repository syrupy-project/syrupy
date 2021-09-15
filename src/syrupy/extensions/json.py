import datetime
import json
from gettext import gettext
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Optional,
)

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
    @property
    def _file_extension(self) -> str:
        return "json"

    @classmethod
    def _filter(
        cls,
        data: SerializableData,
        filtered: SerializableData,
        path: PropertyPath,
        exclude: Optional["PropertyFilter"] = None,
        matcher: Optional[PropertyMatcher] = None,
    ) -> SerializableData:
        if not isinstance(data, dict):
            return data
        for k, v in data.items():
            path_tpl = (*path, (k, type(v)))
            path_str = ".".join(str(p) for p, _ in path_tpl)
            if exclude and exclude(prop=path_str, path=()):
                continue
            if matcher:
                v = matcher(data=v, path=path_tpl)
            if isinstance(v, dict):
                filtered[k] = {}
                filtered[k] = cls._filter(v, filtered[k], path_tpl, exclude, matcher)
            elif isinstance(v, Repr):
                filtered[k] = repr(v)
            elif isinstance(v, datetime.datetime):
                filtered[k] = v.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
            else:
                filtered[k] = v
        return filtered

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> "SerializedData":
        data = self._filter(data, {}, path=(), exclude=exclude, matcher=matcher)
        return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"

    def _read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str
    ) -> Optional[SerializableData]:
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
