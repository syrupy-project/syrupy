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
                "",  # newline at end
            ]
        )


def test_multiline_repr(snapshot):
    assert MultilineRepr() == snapshot


def test_multiline_repr_with_no_indentation(snapshot):
    # snapshot file has been manually edited
    # remove newlines from this test if you update the snapshot
    assert MultilineRepr() == snapshot
