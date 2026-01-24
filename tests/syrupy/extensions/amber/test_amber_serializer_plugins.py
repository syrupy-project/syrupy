""" "Tests for the Amber serializer plugins for attrs, dataclasses, and Pydantic models."""

from dataclasses import dataclass

import attr
import pytest
from pydantic import BaseModel

from syrupy.extensions.amber import AmberSnapshotExtension
from syrupy.extensions.amber.attrs_plugin import AttrsPlugin
from syrupy.extensions.amber.dataclasses_plugin import DataclassPlugin
from syrupy.extensions.amber.pydantic_plugin import PydanticPlugin
from syrupy.extensions.amber.serializer import AmberDataSerializer


# region Data Classes
@attr.s
class AttrsPoint:
    x = attr.ib()
    y = attr.ib()


@dataclass
class DataclassPoint:
    x: int
    y: int


class PydanticPoint(BaseModel):
    x: int
    y: int


class Inner(BaseModel):
    val: int


class ComplexModel(BaseModel):
    """Complex Pydantic model for testing nested structures.

    Note: make sure field names are not sorted alphabetically to test ordering.
    """

    values: list[Inner]

    start: PydanticPoint
    end: PydanticPoint

    mapping: dict[str, Inner]


@dataclass
class Middle:
    inner: Inner
    other: str


@attr.s
class Outer:
    middle = attr.ib()
    tags = attr.ib(factory=list)


# endregion


# region Serializers
class AttrsSerializer(AmberDataSerializer):
    serializer_plugins = [AttrsPlugin]


class DataclassSerializer(AmberDataSerializer):
    serializer_plugins = [DataclassPlugin]


class PydanticSerializer(AmberDataSerializer):
    serializer_plugins = [PydanticPlugin]


class MixedSerializer(AmberDataSerializer):
    serializer_plugins = [AttrsPlugin, DataclassPlugin, PydanticPlugin]


# endregion


# region Extensions
class AmberAttrsExtension(AmberSnapshotExtension):
    serializer_class = AttrsSerializer


class AmberDataclassExtension(AmberSnapshotExtension):
    serializer_class = DataclassSerializer


class AmberPydanticExtension(AmberSnapshotExtension):
    serializer_class = PydanticSerializer


class AmberMixedExtension(AmberSnapshotExtension):
    serializer_class = MixedSerializer


# endregion


# region Fixtures


@pytest.fixture
def snapshot_attrs(snapshot) -> AmberSnapshotExtension:
    return snapshot.use_extension(AmberAttrsExtension)


@pytest.fixture
def snapshot_dataclass(snapshot) -> AmberSnapshotExtension:
    return snapshot.use_extension(AmberDataclassExtension)


@pytest.fixture
def snapshot_pydantic(snapshot) -> AmberSnapshotExtension:
    return snapshot.use_extension(AmberPydanticExtension)


@pytest.fixture
def snapshot_mixed(snapshot) -> AmberSnapshotExtension:
    return snapshot.use_extension(AmberMixedExtension)


# endregion


# region Tests
def test_attrs_plugin(snapshot_attrs):
    """Test serialization of an attrs class using the AmberAttrsExtension."""
    point = AttrsPoint(x=1, y=2)
    assert point == snapshot_attrs


def test_dataclasses_plugin(snapshot_dataclass):
    """Test serialization of a dataclass using the AmberDataclassExtension."""
    point = DataclassPoint(x=1, y=2)
    assert point == snapshot_dataclass


def test_pydantic_plugin(snapshot_pydantic):
    """Test serialization of a Pydantic model using the AmberPydanticExtension."""
    point = PydanticPoint(x=1, y=2)
    assert point == snapshot_pydantic


def test_mixed_plugins(snapshot_mixed):
    """Test serialization of mixed data types using the AmberMixedExtension."""
    complex_data = {
        "attrs": AttrsPoint(x=1, y=2),
        "dataclass": DataclassPoint(x=3, y=4),
        "pydantic": PydanticPoint(x=5, y=6),
        "list_mixed": [
            AttrsPoint(x=10, y=20),
            DataclassPoint(x=30, y=40),
        ],
    }
    assert complex_data == snapshot_mixed


def test_nested_structures(snapshot_mixed):
    """Test serialization of nested structures using the AmberMixedExtension."""
    data = Outer(middle=Middle(inner=Inner(val=42), other="nested"), tags=["c"])
    assert data == snapshot_mixed


def test_complex_pydantic_model(snapshot_pydantic):
    """Test serialization of a complex Pydantic model using the AmberPydanticExtension.

    Ensures nested models, lists, and dicts are handled correctly.
    Ensures field ordering is preserved as defined in the model.
    """
    data = ComplexModel(
        end=PydanticPoint(x=10, y=10),
        mapping={"first": Inner(val=100), "second": Inner(val=200)},
        start=PydanticPoint(x=0, y=0),
        values=[Inner(val=1), Inner(val=2)],
    )
    assert data == snapshot_pydantic


# endregion
