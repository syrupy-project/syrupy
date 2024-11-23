from syrupy.assertion import DiffMode


def test_can_be_stringified(snapshot):
    assert snapshot == str(DiffMode.DETAILED)
    assert snapshot == str(DiffMode.DISABLED)
