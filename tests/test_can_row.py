from types import SimpleNamespace

from app.can_row import CANRow


def make_frame(can_id=0x7E8, data=None, dlc=None):
    if data is None:
        data = bytes([0x01, 0x02, 0x03, 0x04])

    if dlc is None:
        dlc = len(data)

    return SimpleNamespace(
        can_id=can_id,
        dlc=dlc,
        data=data
    )


def test_can_row_creation():

    frame = make_frame(
        data=bytes([0x01, 0x02, 0x03, 0x04])
    )

    row = CANRow(frame)

    assert row.can_id == 0x7E8
    assert row.dlc == 4

    assert row.get_data() == [
        0x01,
        0x02,
        0x03,
        0x04,
    ]


def test_update_changes_byte():

    row = CANRow(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    row.update(
        make_frame(
            data=bytes([0x01, 0x02, 0x22, 0x04])
        )
    )

    assert row.get_data() == [
        0x01,
        0x02,
        0x22,
        0x04,
    ]


def test_changed_byte_is_detected():

    row = CANRow(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    row.update(
        make_frame(
            data=bytes([0x01, 0x02, 0x22, 0x04])
        )
    )

    assert row.get_changed_bytes() == [2]


def test_is_byte_changed():

    row = CANRow(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    row.update(
        make_frame(
            data=bytes([0x01, 0x02, 0x22, 0x04])
        )
    )

    assert row.is_byte_changed(0) is False
    assert row.is_byte_changed(1) is False
    assert row.is_byte_changed(2) is True
    assert row.is_byte_changed(3) is False


def test_same_data_is_not_changed():

    row = CANRow(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    row.update(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    assert row.get_changed_bytes() == []

    for index in range(4):
        assert row.is_byte_changed(index) is False


def test_get_byte():

    row = CANRow(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    assert row.get_byte(0) == 0x01
    assert row.get_byte(1) == 0x02
    assert row.get_byte(2) == 0x03
    assert row.get_byte(3) == 0x04


def test_get_byte_out_of_range():

    row = CANRow(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    assert row.get_byte(-1) is None
    assert row.get_byte(4) is None
    assert row.get_byte(100) is None


def test_is_byte_changed_out_of_range():

    row = CANRow(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    assert row.is_byte_changed(-1) is False
    assert row.is_byte_changed(4) is False
    assert row.is_byte_changed(100) is False


def test_dlc_update():

    row = CANRow(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    row.update(
        make_frame(
            data=bytes([0xAA, 0xBB]),
            dlc=2
        )
    )

    assert row.dlc == 2

    assert row.get_data() == [
        0xAA,
        0xBB,
    ]


def test_new_bytes_are_added():

    row = CANRow(
        make_frame(
            data=bytes([0x01, 0x02])
        )
    )

    row.update(
        make_frame(
            data=bytes([0x01, 0x02, 0x03, 0x04])
        )
    )

    assert row.get_data() == [
        0x01,
        0x02,
        0x03,
        0x04,
    ]
