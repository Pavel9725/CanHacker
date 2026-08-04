from types import SimpleNamespace

from app.can_model import CANModel


def make_frame(
    can_id=0x7E8,
    data=None,
    dlc=None
):
    if data is None:
        data = bytes([
            0x01,
            0x02,
            0x03,
            0x04,
        ])

    if dlc is None:
        dlc = len(data)

    return SimpleNamespace(
        can_id=can_id,
        dlc=dlc,
        data=data
    )


def test_model_starts_empty():

    model = CANModel()

    assert model.get_all() == []
    assert model.get_ids() == []
    assert len(model) == 0


def test_new_frame_creates_row():

    model = CANModel()

    frame = make_frame(
        can_id=0x7E8,
        data=bytes([0x01, 0x02, 0x03, 0x04])
    )

    model.handle_frame(frame)

    assert len(model) == 1
    assert model.get_ids() == [0x7E8]


def test_get_row_returns_row():

    model = CANModel()

    frame = make_frame(
        can_id=0x7E8,
        data=bytes([0x01, 0x02, 0x03, 0x04])
    )

    model.handle_frame(frame)

    row = model.get_row(0x7E8)

    assert row is not None
    assert row.can_id == 0x7E8


def test_get_unknown_row_returns_none():

    model = CANModel()

    assert model.get_row(0x7E8) is None


def test_get_data():

    model = CANModel()

    frame = make_frame(
        can_id=0x7E8,
        data=bytes([0x01, 0x02, 0x03, 0x04])
    )

    model.handle_frame(frame)

    assert model.get_data(0x7E8) == [
        0x01,
        0x02,
        0x03,
        0x04,
    ]


def test_get_unknown_data_returns_none():

    model = CANModel()

    assert model.get_data(0x7E8) is None


def test_same_id_updates_existing_row():

    model = CANModel()

    first_frame = make_frame(
        can_id=0x7E8,
        data=bytes([0x01, 0x02, 0x03, 0x04])
    )

    second_frame = make_frame(
        can_id=0x7E8,
        data=bytes([0x01, 0x02, 0x22, 0x04])
    )

    model.handle_frame(first_frame)
    model.handle_frame(second_frame)

    assert len(model) == 1

    assert model.get_data(0x7E8) == [
        0x01,
        0x02,
        0x22,
        0x04,
    ]


def test_different_ids_create_different_rows():

    model = CANModel()

    frame_1 = make_frame(
        can_id=0x7E8,
        data=bytes([0x01, 0x02, 0x03, 0x04])
    )

    frame_2 = make_frame(
        can_id=0x7EA,
        data=bytes([0xAA, 0xBB, 0xCC, 0xDD])
    )

    model.handle_frame(frame_1)
    model.handle_frame(frame_2)

    assert len(model) == 2

    assert model.get_ids() == [
        0x7E8,
        0x7EA,
    ]


def test_get_all_returns_all_rows():

    model = CANModel()

    frame_1 = make_frame(
        can_id=0x7E8,
        data=bytes([0x01, 0x02, 0x03, 0x04])
    )

    frame_2 = make_frame(
        can_id=0x7EA,
        data=bytes([0xAA, 0xBB, 0xCC, 0xDD])
    )

    model.handle_frame(frame_1)
    model.handle_frame(frame_2)

    rows = model.get_all()

    assert len(rows) == 2

    assert rows[0].can_id == 0x7E8
    assert rows[1].can_id == 0x7EA


def test_changed_bytes():

    model = CANModel()

    first_frame = make_frame(
        can_id=0x7E8,
        data=bytes([0x01, 0x02, 0x03, 0x04])
    )

    second_frame = make_frame(
        can_id=0x7E8,
        data=bytes([0x01, 0x02, 0x22, 0x04])
    )

    model.handle_frame(first_frame)
    model.handle_frame(second_frame)

    assert model.get_changed_bytes(0x7E8) == [2]


def test_unknown_changed_bytes_returns_empty_list():

    model = CANModel()

    assert model.get_changed_bytes(0x7E8) == []
