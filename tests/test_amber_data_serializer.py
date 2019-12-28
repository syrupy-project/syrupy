import pytest

from syrupy.serializers.amber import DataSerializer


@pytest.mark.parametrize(
    "data",
    ["some string", "string with 'quotes'", r"Raw string", ["a", "list", 1, 2]],
    ids=lambda x: "",
)
def test_does_not_fail(data):
    DataSerializer.serialize(data)


class SomeClass:
    pass


@pytest.mark.parametrize(
    "data",
    ["a string", 123, (1, 2), True, None, dict(), frozenset(), SomeClass()],
    ids=lambda x: "",
)
def test_produces_valid_object_types(snapshot, data):
    assert snapshot == DataSerializer.object_type(data)
