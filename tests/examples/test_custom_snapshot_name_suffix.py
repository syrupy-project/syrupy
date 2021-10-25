def test_snapshot_custom_snapshot_name_suffix(snapshot):
    assert "Syrupy is amazing!" == snapshot(name="test_is_amazing")
    assert "Syrupy is awesome!" == snapshot(name="test_is_awesome")
