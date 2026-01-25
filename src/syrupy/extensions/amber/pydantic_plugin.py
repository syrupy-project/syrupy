"""Pydantic plugin for Syrupy Amber serializer."""

from typing import Any

from pydantic import BaseModel

from syrupy.extensions.amber.serializer import (
    AmberDataSerializer,
    AmberDataSerializerPlugin,
    attr_getter,
)
from syrupy.types import SerializableData


class PydanticPlugin(AmberDataSerializerPlugin):
    """A Syrupy extension that serializes Pydantic models using Amber format."""

    @classmethod
    def is_data_serializable(cls, data: "SerializableData") -> bool:
        """Check if the data is a Pydantic BaseModel instance."""
        return isinstance(data, BaseModel)

    @classmethod
    def serialize(cls, data: BaseModel, **kwargs: Any) -> str:
        """Serialize a Pydantic BaseModel instance into Amber format.

        Uses the model's defined fields to ensure consistent ordering.
        """
        keys = [name for name, _ in data]
        return AmberDataSerializer.serialize_custom_iterable(
            data=data,
            resolve_entries=(keys, attr_getter, None),
            separator="=",
            **kwargs,
        )
