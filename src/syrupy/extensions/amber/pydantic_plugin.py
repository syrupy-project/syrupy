from pydantic import BaseModel

from syrupy.extensions.amber.serializer import (
    AmberDataSerializer,
    AmberDataSerializerPlugin,
    attr_getter,
)
from syrupy.types import SerializableData


class PydanticPlugin(AmberDataSerializerPlugin):
    """A Syrupy extension that serializes Pydantic models to JSON-compatible dicts
    before snapshotting.
    """

    @classmethod
    def __plugin_can_serialize__(cls, data: "SerializableData") -> bool:
        return isinstance(data, BaseModel)

    @classmethod
    def __plugin_serialize__(cls, data: BaseModel, **kwargs) -> str:
        keys = type(data).model_fields.keys()

        return AmberDataSerializer.serialize_custom_iterable(
            data=data,
            resolve_entries=(keys, attr_getter, None),
            separator="=",
            **kwargs,
        )