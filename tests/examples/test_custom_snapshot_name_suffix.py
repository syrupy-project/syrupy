def test_snapshot_custom_snapshot_name_suffix(snapshot):
    assert "Syrupy is amazing!" == snapshot(snapshot_name_suffix="test_is_amazing")
    assert "Syrupy is awesome!" == snapshot(snapshot_name_suffix="test_is_awesome")
