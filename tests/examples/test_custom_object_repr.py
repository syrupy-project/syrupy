import attr


@attr.s
class MyCustomReprClass:
    prop1 = attr.ib(default=1)
    prop2 = attr.ib(default="a")
    prop3 = attr.ib(default={1, 2, 3})


def test_snapshot_attr_class(snapshot):
    assert MyCustomReprClass() == snapshot


class MyCustomSmartReprClass:
    prop1 = 1
    prop2 = "a"
    prop3 = {1, 2, 3}

    def __repr__(self):
        state = "\n".join(
            f"  {a}={getattr(self, a)}" for a in dir(self) if not a.startswith("__")
        )
        return f"{self.__class__.__name__}(\n{state}\n)"


def test_snapshot_smart_class(snapshot):
    assert MyCustomSmartReprClass() == snapshot
