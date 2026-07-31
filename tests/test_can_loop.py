from app.can_frame import CANFrame, build_packet
from app.can_parser import CANParser


def test_can_frame_build_and_parse():

    original = CANFrame(0x7E8, 8, bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]))

    packet = build_packet(original)

    parser = CANParser()

    frames = parser.feed(packet)

    assert len(frames) == 1

    received = frames[0]

    assert received.can_id == original.can_id

    assert received.dlc == original.dlc

    assert received.data == original.data