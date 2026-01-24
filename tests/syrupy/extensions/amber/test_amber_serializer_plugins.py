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
def snapshot_attrs(snapshot):
    return snapshot.use_extension(AmberAttrsExtension)


@pytest.fixture
def snapshot_dataclass(snapshot):
    return snapshot.use_extension(AmberDataclassExtension)


@pytest.fixture
def snapshot_pydantic(snapshot):
    return snapshot.use_extension(AmberPydanticExtension)


@pytest.fixture
def snapshot_mixed(snapshot):
    return snapshot.use_extension(AmberMixedExtension)


# endregion


# region Tests
def test_attrs_plugin(snapshot_attrs):
    point = AttrsPoint(x=1, y=2)
    assert point == snapshot_attrs


def test_dataclasses_plugin(snapshot_dataclass):
    point = DataclassPoint(x=1, y=2)
    assert point == snapshot_dataclass


def test_pydantic_plugin(snapshot_pydantic):
    point = PydanticPoint(x=1, y=2)
    assert point == snapshot_pydantic


def test_mixed_plugins(snapshot_mixed):
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
    data = Outer(middle=Middle(inner=Inner(val=42), other="nested"), tags=["c"])
    assert data == snapshot_mixed


# endregion
