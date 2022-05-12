import json
from datetime import datetime
from numbers import Number
from types import GeneratorType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Hashable,
    Iterable,
    List,
    Optional,
    Union,
)

from syrupy.extensions.amber.serializer import (
    DataSerializer,
    PreppedData,
)
from syrupy.extensions.single_file import (
    SingleFileSnapshotExtension,
    WriteMode,
)

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
    _write_mode = WriteMode.TEXT

    @property
    def _file_extension(self) -> str:
        return "json"

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> "SerializedData":
        def matcher_with_datetime(
            *, data: "SerializableData", path: "PropertyPath"
        ) -> Optional[SerializableData]:
            matched_data = matcher(data=data, path=path) if matcher else data
            if data is not matched_data:
                return matched_data
            if isinstance(data, (datetime,)):
                return data.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
            return data

        prepped_data = DataSerializer._prepare(
            data=data, exclude=exclude, matcher=matcher_with_datetime
        )
        return (
            json.dumps(
                prepped_data,
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
                cls=JSONSnapshotEncoder,
            )
            + "\n"
        )


JSONValue = Union[str, Number, bool, None, List[Any], Dict[str, Any]]
PyJSONArray = (frozenset, list, set, tuple, GeneratorType)


class JSONSnapshotEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, PreppedData):
            return self.prep_data_as_json(o)
        return super().default(o)

    def prep_data_as_json(self, o: "PreppedData") -> "JSONValue":
        if isinstance(o.value, (bool,)) or o.value is None:
            return o.value

        if isinstance(o.value, str):
            if issubclass(o.value_type, (Number,)):
                return o.value_type(o.value)  # type: ignore
            return o.value

        if isinstance(o.value, Iterable):
            prepped_data = (item for item in o.value if isinstance(item, PreppedData))
            if issubclass(o.value_type, (str,)):
                return "".join(str(item.value) for item in prepped_data)
            if issubclass(o.value_type, PyJSONArray) and not o.is_namedtuple:
                return [self.default(item) for item in o.value]

            def serialize_key(key: Union[Hashable, None]) -> str:
                if key is None or isinstance(key, str):
                    return str(key)
                return "".join(
                    line.strip() for line in DataSerializer.serialize(key).splitlines()
                )

            return {
                serialize_key(item.key): self.default(item) for item in prepped_data
            }

        return None
