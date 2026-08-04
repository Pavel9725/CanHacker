import time
from app.byte_state import ByteState


def test_initial_value():
    byte = ByteState(0x03)

    assert byte.value == 0x03
    assert byte.changed_at is None


def test_update_changes_value():
    byte = ByteState(0x03)

    result = byte.update(0x22)

    assert result is True
    assert byte.value == 0x22
    assert byte.changed_at is not None


def test_update_same_value_does_not_change():
    byte = ByteState(0x03)

    result = byte.update(0x03)

    assert result is False
    assert byte.value == 0x03
    assert byte.changed_at is None


def test_is_changed_after_update():
    byte = ByteState(0x03)

    byte.update(0x22)

    assert byte.is_changed() is True


def test_is_changed_initially_false():
    byte = ByteState(0x03)

    assert byte.is_changed() is False


def test_is_changed_after_timeout():
    byte = ByteState(0x03)

    byte.update(0x22)

    time.sleep(
        ByteState.CHANGE_DISPLAY_TIME + 0.05
    )

    assert byte.is_changed() is False

