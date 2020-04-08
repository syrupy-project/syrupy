# type: ignore
import base64
from collections import namedtuple

import pytest

from syrupy.extensions.image import (
    PNGImageSnapshotExtension,
    SVGImageSnapshotExtension,
)


example_cycle_list = [1, 2, 3]
example_cycle_list.append(example_cycle_list)
example_cycle_dict = {"a": 1, "b": 2, "c": 3}
example_cycle_dict.update(d=example_cycle_dict)
example_png = base64.b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAADIAAAAyBAMAAADsEZWCAAAAG1BMVEXMzMy"
    b"Wlpaqqqq3t7exsbGcnJy+vr6jo6PFxcUFpPI/AAAACXBIWXMAAA7EAAAOxA"
    b"GVKw4bAAAAQUlEQVQ4jWNgGAWjgP6ASdncAEaiAhaGiACmFhCJLsMaIiDAE"
    b"QEi0WXYEiMCOCJAJIY9KuYGTC0gknpuHwXDGwAA5fsIZw0iYWYAAAAASUVO"
    b"RK5CYII="
)
example_svg = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<svg viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">'
    '<g><rect width="50" height="50" fill="#fff"/>'
    '<g><g fill="#fff" stroke="#707070">'
    '<rect width="50" height="50" stroke="none"/>'
    '<rect x="0" y="0" width="50" height="50" fill="none"/></g>'
    '<text transform="translate(10 27)" fill="#707070" '
    'font-family="ConsolasForPowerline, Consolas for Powerline" font-size="8">'
    '<tspan x="0" y="0">50 x 50</tspan></text></g></g></svg>'
)
ExampleTuple = namedtuple("ExampleTuple", ["a", "b", "c", "d"])


class ExampleClass:
    a = 1
    b = "2"
    c = example_cycle_list
    d = example_cycle_dict
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


test_cases = [
    False,
    True,
    3.5,
    7,
    2 / 6,
    22 / 7,
    "",
    r"Raw string",
    r"Escaped \n",
    r"Backslash \u U",
    "🥞🐍🍯",
    "singleline:",
    "- singleline",
    "line 1\nline 2\nline 3",
    "line 2\nline 2\n  line 3",
    "line 1\r\nline 2\r\nline 3",
    "string with 'quotes'",
    b"Byte string",
    ("this", "is", ("a", "tuple")),
    ExampleTuple(a="this", b="is", c="a", d={"named", "tuple"}),
    {"this", "is", "a", "set"},
    {"contains", "frozen", frozenset({"1", "2"})},
    {"contains", "tuple", (1, 2)},
    {"contains", "namedtuple", ExampleTuple(a=1, b=2, c=3, d=4)},
    {"b": True, "c": "Some text.", "d": ["1", 2], "a": {"e": False}},
    {"b": True, "c": "Some ttext.", "d": ["1", 2], "a": {"e": False}},
    {
        1: True,
        "a": "Some ttext.",
        frozenset({"1", "2"}): ["1", 2],
        ExampleTuple(a=1, b=2, c=3, d=4): {"e": False},
    },
    [1, 2, "string", {"key": "value"}],
    example_cycle_list,
    example_cycle_dict,
    ExampleClass(ExampleClass()),
]


class TestClass:
    def test_method(self, snapshot):
        assert example_svg == snapshot(extension_class=SVGImageSnapshotExtension)
        assert example_svg == snapshot
        assert example_png == snapshot(extension_class=PNGImageSnapshotExtension)

    @pytest.mark.parametrize(
        "actual", test_cases, ids=lambda x: "",
    )
    def test_parametrized_method(self, snapshot, actual):
        assert actual == snapshot
        snapshot.assert_match(actual)
        assert snapshot == actual

    @pytest.mark.parametrize(
        "actual", test_cases, ids=lambda x: "",
    )
    class TestNestedParametrizedClass:
        def test_nested_method(self, snapshot, actual):
            assert snapshot == actual
