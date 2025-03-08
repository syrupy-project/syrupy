class ReprWithNewline:
    def __init__(self, newlines: int = 1) -> None:
        self.newlines = newlines

    def __repr__(self) -> str:
        newlines = "\n" * self.newlines
        return f"ReprWithNewline{newlines}"


def test_trailing_no_newline_in_repr(snapshot):
    assert ReprWithNewline(0) == snapshot


def test_trailing_newline_in_repr(snapshot):
    assert ReprWithNewline(1) == snapshot


def test_trailing_2_newlines_in_repr(snapshot):
    assert ReprWithNewline(2) == snapshot


class MultilineRepr:
    def __repr__(self) -> str:
        return "\n".join(
            [
                "Line1",
                "Line2\n",  # extra newline
                "Line3 ",  # with an extra space
            ]
        )


def test_multiline_repr(snapshot):
    assert MultilineRepr() == snapshot
