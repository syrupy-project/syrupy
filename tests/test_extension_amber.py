from collections import namedtuple

import pytest


def test_non_snapshots(snapshot):
    with pytest.raises(AssertionError):
        assert "Lorem ipsum." == "Muspi merol."


def test_reflection(snapshot):
    assert snapshot == snapshot


def test_empty_snapshot(snapshot):
    assert snapshot == None  # noqa: E711
    assert snapshot == ""


def test_newline_control_characters(snapshot):
    assert snapshot == "line 1\nline 2"
    assert snapshot == "line 1\r\nline 2"
    assert snapshot == "line 1\r\nline 2\r\n"


def test_multiline_string_in_dict(snapshot):
    lines = "\n".join(["line 1", "line 2"])
    assert {"value": lines} == snapshot


def test_deeply_nested_multiline_string_in_dict(snapshot):
    lines = "\n".join(["line 1", "line 2", "line 3"])
    d = {"value_a": {"value_b": lines}}
    assert d == snapshot


@pytest.mark.parametrize("actual", [False, True])
def test_bool(actual, snapshot):
    assert actual == snapshot


@pytest.mark.parametrize(
    "actual",
    [
        "",
        r"Raw string",
        r"Escaped \n",
        r"Backslash \u U",
        "🥞🐍🍯",
        "singleline:",
        "- singleline",
        "multi-line\nline 2\nline 3",
        "multi-line\nline 2\n  line 3",
        "string with 'quotes'",
        b"Byte string",
    ],
    ids=lambda x: "",
)
def test_string(snapshot, actual):
    assert snapshot == actual


def test_multiple_snapshots(snapshot):
    assert "First." == snapshot
    snapshot.assert_match("Second.")
    assert snapshot == "Third."


ExampleTuple = namedtuple("ExampleTuple", ["a", "b", "c", "d"])


def test_tuple(snapshot):
    assert snapshot == ("this", "is", ("a", "tuple"))
    assert snapshot == ExampleTuple(a="this", b="is", c="a", d={"named", "tuple"})


@pytest.mark.parametrize(
    "actual",
    [
        {"this", "is", "a", "set"},
        {"contains", "frozen", frozenset({"1", "2"})},
        {"contains", "tuple", (1, 2)},
        {"contains", "namedtuple", ExampleTuple(a=1, b=2, c=3, d=4)},
    ],
)
def test_set(snapshot, actual):
    assert snapshot == actual


@pytest.mark.parametrize(
    "actual",
    [
        {"b": True, "c": "Some text.", "d": ["1", 2], "a": {"e": False}},
        {"b": True, "c": "Some ttext.", "d": ["1", 2], "a": {"e": False}},
        {
            1: True,
            "a": "Some ttext.",
            frozenset({"1", "2"}): ["1", 2],
            ExampleTuple(a=1, b=2, c=3, d=4): {"e": False},
        },
    ],
)
def test_dict(snapshot, actual):
    assert actual == snapshot


def test_numbers(snapshot):
    assert snapshot == 3.5
    assert snapshot == 7
    assert snapshot == 2 / 6


def test_list(snapshot):
    assert snapshot == [1, 2, "string", {"key": "value"}]


list_cycle = [1, 2, 3]
list_cycle.append(list_cycle)

dict_cycle = {"a": 1, "b": 2, "c": 3}
dict_cycle.update(d=dict_cycle)


@pytest.mark.parametrize("cyclic", [list_cycle, dict_cycle])
def test_cycle(cyclic, snapshot):
    assert cyclic == snapshot


class CustomClass:
    a = 1
    b = "2"
    c = list_cycle
    d = dict_cycle
    _protected_variable = None
    __private_variable = None

    def __init__(self, x=None):
        self.x = x
        self._y = 1
        self.__z = 2

    def public_method(self, a, b=1, *, c, d=None):
        pass

    def _protected_method(self):
        pass

    def __private_method(self):
        pass


def test_custom_object_repr(snapshot):
    assert CustomClass(CustomClass()) == snapshot


class TestClass:
    def test_class_method_name(self, snapshot):
        assert snapshot == "this is in a test class"

    @pytest.mark.parametrize("actual", ["a", "b", "c"])
    def test_class_method_parametrized(self, snapshot, actual):
        assert snapshot == actual

    @pytest.mark.parametrize("actual", ["x", "y", "z"])
    class TestNestedClass:
        def test_nested_class_method(self, snapshot, actual):
            assert snapshot == f"parameterized nested class method {actual}"


class TestSubClass(TestClass):
    pass


@pytest.mark.parametrize("parameter_with_dot", ("value.with.dot",))
def test_parameter_with_dot(parameter_with_dot, snapshot):
    assert parameter_with_dot == snapshot


@pytest.mark.parametrize("parameter_1", ("foo",))
@pytest.mark.parametrize("parameter_2", ("bar",))
def test_doubly_parametrized(parameter_1, parameter_2, snapshot):
    assert parameter_1 == snapshot
    assert parameter_2 == snapshot
