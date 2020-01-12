class MyCustomClass:
    prop1 = 1
    prop2 = "a"
    prop3 = {1, 2, 3}


def test_snapshot_custom_class(snapshot):
    assert MyCustomClass() == snapshot


class MyCustomReprClass(MyCustomClass):
    def __repr__(self):
        state = "\n".join(
            f"  {a}={repr(getattr(self, a))},"
            for a in sorted(dir(self))
            if not a.startswith("_")
        )
        return f"{self.__class__.__name__}(\n{state}\n)"


def test_snapshot_custom_repr_class(snapshot):
    assert MyCustomReprClass() == snapshot
