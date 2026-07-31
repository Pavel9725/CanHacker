from app.can_parser import CANParser
from app.can_frame import CANFrame, build_packet
from app.crc import crc8_sae_j1850

def test_parser_valid_packet():

    parser = CANParser()

    packet = bytes.fromhex("55 AA 07 E8 08 01 02 03 04 05 06 07 08 D3")

    frames = parser.feed(packet)

    assert len(frames) == 1

    frame = frames[0]

    assert frame.can_id == 0x7E8
    assert frame.dlc == 8
    assert frame.data == bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

def test_parser_garbage():

    parser = CANParser()

    packet = bytes.fromhex("12 FF 33 55 AA 07 E8 08 01 02 03 04 05 06 07 08 D3")

    frames = parser.feed(packet)

    assert len(frames) == 1

    frame = frames[0]

    assert frame.can_id == 0x7E8
    assert frame.dlc == 8
    assert frame.data == bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

def test_parser_packet_in_parts():

    parser = CANParser()

    part1 = bytes.fromhex("55 AA 07 E8 08")
    part2 = bytes.fromhex("01 02 03 04 05 06 07 08 D3")

    frames = parser.feed(part1)

    assert len(frames) == 0

    frames = parser.feed(part2)

    assert len(frames) == 1

    frame = frames[0]

    assert frame.can_id == 0x7E8
    assert frame.dlc == 8
    assert frame.data == bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

def test_parser_bad_crc():

    parser = CANParser()

    packet = bytes.fromhex("55 AA 07 E8 08 01 02 03 04 05 06 07 08 FF")

    frames = parser.feed(packet)

    assert len(frames) == 0


def test_parser_multiple_packets():
    parser = CANParser()

    packet1= bytes.fromhex("55 AA 07 E8 08 01 02 03 04 05 06 07 08 D3")
    packet2 = bytes.fromhex("55 AA 07 E9 08 10 20 30 40 50 60 70 80 CA")
    packet3 = bytes.fromhex("55 AA 07 EA 08 AA BB CC DD 11 22 33 44 38")

    data = packet1 + packet2 + packet3

    frames = parser.feed(data)

    assert len(frames) == 3

    assert frames[0].can_id == 0x7E8
    assert frames[0].data == bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

    assert frames[1].can_id == 0x7E9
    assert frames[1].data == bytes([0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80])

    assert frames[2].can_id == 0x7EA
    assert frames[2].data == bytes([0xAA, 0xBB, 0xCC, 0xDD, 0x11, 0x22, 0x33, 0x44])

