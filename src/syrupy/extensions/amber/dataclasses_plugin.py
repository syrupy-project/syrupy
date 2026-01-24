import dataclasses
from typing import Any

from syrupy.extensions.amber.serializer import (
    AmberDataSerializer,
    AmberDataSerializerPlugin,
    attr_getter,
)
from syrupy.types import SerializableData


class DataclassPlugin(AmberDataSerializerPlugin):
    """A Syrupy extension that serializes dataclasses to JSON-compatible dicts
    before snapshotting.
    """

    @classmethod
    def is_data_serializable(cls, data: "SerializableData") -> bool:
        return dataclasses.is_dataclass(data) and not isinstance(data, type)

    @classmethod
    def serialize(cls, data: "SerializableData", **kwargs: Any) -> str:
        keys = sorted([f.name for f in dataclasses.fields(data)])

        return AmberDataSerializer.serialize_custom_iterable(
            data=data,
            resolve_entries=(keys, attr_getter, None),
            separator="=",
            **kwargs,
        )
