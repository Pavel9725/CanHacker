from crc import crc8_sae_j1850


class CANFrame:

    def __init__(self, can_id: int, data: bytes):
        self.can_id = can_id
        self.data = data
        self.dlc = len(data)


def build_packet(frame: CANFrame) -> bytes:
        packet = bytearray()

        #packet.append(0x55)
        #acket.append(0xAA)

        packet.extend(frame.can_id.to_bytes(2, byteorder='big'))

        packet.append((frame.dlc))

        packet.extend(frame.data)

        crc_data = packet[2:]

        crc = crc8_sae_j1850(crc_data)

        packet.append(crc)

        return bytes(packet)

