class CANFrame:

    def __init__(self, can_id: int, data: bytes):
        self.can_id = can_id
        self.data = data
        self.dlc = len(data)


    def __str__(self):
        return (
            f"CAN ID: 0x{self.can_id:X}, "
            f"DLC: {self.dlc}, "
            f"DATA: {self.data.hex(' ')}"
        )

def build_packet(frame: CANFrame) -> bytes:
        packet = bytearray()

        packet.append(0xAA)

        packet.extend(frame.can_id.to_bytes(2, byteorder='big'))

        packet.append((frame.dlc))

        packet.extend(frame.data)

        return bytes(packet)

frame = CANFrame(
    0x7E8,
    bytes([
        0x11,
        0x22,
        0x33,
        0x44,
        0x55,
        0x66,
        0x77,
        0x88
    ])
)

packet = build_packet(frame)
