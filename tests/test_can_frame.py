from app.can_frame import CANFrame, build_packet
from app.crc import crc8_sae_j1850
import pytest


def test_can_frame_id():
    frame = CANFrame(0x7E8, 3, bytes([0x01, 0x02, 0x03]))
    assert frame.can_id == 0x7E8

def test_can_frame_data():
    data = bytes([0x01, 0x02, 0x03])

    frame = CANFrame(0x7E8, 3, data)
    assert frame.data == data

def test_can_frame_dlc():
    frame = CANFrame(0x7E8, 4, bytes([0x01, 0x02, 0x03, 0x04]))
    assert frame.dlc == 4

def test_can_frame_empty_data():

    frame = CANFrame(0x7E8, 0, bytes())
    assert frame.dlc == 0

def test_build_packet_start_bytes():
    frame = CANFrame(0x7E8, 3, bytes([0x01, 0x02, 0x03]))
    packet = build_packet(frame)
    assert packet[0] == 0x55
    assert packet[1] == 0xAA

def test_build_packet_can_id():
    frame = CANFrame(0x7E8, 3, bytes([0x01, 0x02, 0x03]))
    packet = build_packet(frame)
    assert packet[2] == 0x07
    assert packet[3] == 0xE8

def test_build_packet_dlc():
    frame = CANFrame(0x7E8, 3, bytes([0x01, 0x02, 0x03]))
    packet = build_packet(frame)
    assert packet[4] == 3

def test_build_packet_data():
    data = bytes([0x01, 0x02, 0x03])
    frame = CANFrame(0x7E8, 3, data)
    packet = build_packet(frame)
    assert packet[5:8] == data

def test_build_packet_crc():
    frame = CANFrame(0x7E8, 3, bytes([0x01, 0x02, 0x03]))
    packet = build_packet(frame)
    crc = packet[-1]
    assert crc == crc8_sae_j1850(packet[2:-1])

def test_can_frame_wrong_dlc():

    with pytest.raises(ValueError):
        CANFrame(0x7E8, 8, bytes([0x01,0x02]))



