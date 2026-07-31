from app.can_parser import CANParser
from app.can_logger import CANLogger
from app.can_frame import CANFrame, build_packet


def test_parser_to_logger_flow():
    parser = CANParser()
    logger = CANLogger()

    frame1 = CANFrame(0x7E8, 3, bytes([1,2,3]))
    packet1 = build_packet(frame1)

    frames = parser.feed(packet1)

    assert len(frames) == 1

    logger.log(frames[0])

    assert frames[0].can_id == 0x7E8
    assert frames[0].data == bytes([1,2,3])

def test_parser_to_logger_detect_change():
    parser = CANParser()
    logger = CANLogger()

    frame1 = CANFrame(0x7E8, 3, bytes([1,2,3]))
    frame2 = CANFrame(0x7E8, 3, bytes([1,0xFF,3]))

    logger.log(parser.feed(build_packet(frame1))[0])
    logger.log(parser.feed(build_packet(frame2))[0])

    history = logger.history[0x7E8]

    assert len(history) == 1
    assert history[0]["type"] == "byte"
    assert history[0]["index"] == 1
    assert history[0]["old"] == 2
    assert history[0]["new"] == 0xFF