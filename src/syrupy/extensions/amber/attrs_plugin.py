from typing import Any

import attr

from syrupy.extensions.amber.serializer import (
    AmberDataSerializer,
    AmberDataSerializerPlugin,
    attr_getter,
)
from syrupy.types import SerializableData


class AttrsPlugin(AmberDataSerializerPlugin):
    """A Syrupy extension that serializes attrs classes to JSON-compatible dicts
    before snapshotting.
    """

    @classmethod
    def is_data_serializable(cls, data: "SerializableData") -> bool:
        return attr.has(type(data))

    @classmethod
    def serialize(cls, data: "SerializableData", **kwargs: Any) -> str:
        keys = sorted([a.name for a in attr.fields(type(data))])

        return AmberDataSerializer.serialize_custom_iterable(
            data=data,
            resolve_entries=(keys, attr_getter, None),
            separator="=",
            **kwargs,
        )
