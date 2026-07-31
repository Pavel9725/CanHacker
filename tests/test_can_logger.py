from app.can_logger import CANLogger
from app.can_frame import CANFrame


def test_logger_new_id():
    logger = CANLogger()

    frame = CANFrame(0x7E8, 3, bytes([1,2,3]))
    logger.log(frame)

    assert 0x7E8 in logger.last_frames
    assert logger.last_frames[0x7E8].data == bytes([1,2,3])
    assert 0x7E8 not in logger.history

def test_logger_same_frame_no_changes():
    logger = CANLogger()

    frame1 = CANFrame(0x7E8, 3, bytes([1, 2, 3]))
    frame2 = CANFrame(0x7E8, 3, bytes([1, 2, 3]))

    logger.log(frame1)
    logger.log(frame2)

    assert 0x7E8 not in logger.history

def test_logger_byte_change():
    logger = CANLogger()

    frame1 = CANFrame(0x7E8, 3, bytes([1, 2, 3]))
    frame2 = CANFrame(0x7E8, 3, bytes([1, 0xFF, 3]))

    logger.log(frame1)
    logger.log(frame2)

    assert 0x7E8 in logger.history

    history = logger.history[0x7E8]

    assert len(history) == 1

    change = history[0]

    assert change["index"] == 1
    assert change["old"] == 2
    assert change["new"] == 0xFF

def test_logger_multiple_byte_changes():
    logger = CANLogger()

    frame1 = CANFrame(0x7E8, 4, bytes([1,2,3,4]))
    frame2 = CANFrame(0x7E8, 4, bytes([1,0xFF,0xAA,4]))

    logger.log(frame1)
    logger.log(frame2)

    history = logger.history[0x7E8]

    assert len(history) == 2

    assert history[0]["index"] == 1
    assert history[0]["old"] == 2
    assert history[0]["new"] == 0xFF

    assert history[1]["index"] == 2
    assert history[1]["old"] == 3
    assert history[1]["new"] == 0xAA

def test_logger_separate_ids():
    logger = CANLogger()

    frame1 = CANFrame(0x7E8, 3, bytes([1,2,3]))
    frame2 = CANFrame(0x123, 3, bytes([10,20,30]))
    frame3 = CANFrame(0x7E8, 3, bytes([1,0xFF,3]))

    logger.log(frame1)
    logger.log(frame2)
    logger.log(frame3)

    assert 0x7E8 in logger.history
    assert 0x123 not in logger.history

    change = logger.history[0x7E8][0]

    assert change["index"] == 1
    assert change["old"] == 2
    assert change["new"] == 0xFF

def test_logger_dlc_growth():
    logger = CANLogger()

    frame1 = CANFrame(0x7E8, 2, bytes([1,2]))
    frame2 = CANFrame(0x7E8, 4, bytes([1,2,3,4]))

    logger.log(frame1)
    logger.log(frame2)

    assert 0x7E8 in logger.history

    history = logger.history[0x7E8]

    assert len(history) == 3

def test_logger_dlc_change_record():
    logger = CANLogger()

    frame1 = CANFrame(0x7E8, 1, bytes([0x10]))
    frame2 = CANFrame(0x7E8, 2, bytes([0x10, 0x20]))

    logger.log(frame1)
    logger.log(frame2)

    change = logger.history[0x7E8][0]

    assert change["type"] == "dlc"
    assert change["old"] == 1
    assert change["new"] == 2


def test_logger_dlc_reduce():
    logger = CANLogger()

    frame1 = CANFrame(0x7E8, 4, bytes([1,2,3,4]))
    frame2 = CANFrame(0x7E8, 2, bytes([1,2]))

    logger.log(frame1)
    logger.log(frame2)

    history = logger.history[0x7E8]

    assert len(history) == 3

    assert history[1]["old"] == 3
    assert history[1]["new"] is None

    assert history[2]["old"] == 4
    assert history[2]["new"] is None