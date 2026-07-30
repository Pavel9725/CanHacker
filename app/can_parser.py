from can_frame import CANFrame, build_packet
from crc import crc8_sae_j1850

START_BYTE_1 = 0x55
START_BYTE_2 = 0xAA


class CANParser:


    def __init__(self):
        self.buffer = bytearray()


    def feed(self, data):
        self.buffer += data
        frames = []

        # ищем начало пакета
        while len(self.buffer)  >= 5:
            if self.buffer[0] == START_BYTE_1 and self.buffer[1] == START_BYTE_2:
                dlc = int(self.buffer[4])

                packet_length = 2 + 2 + 1 + dlc + 1

                if len(self.buffer) >= packet_length:
                    packet = self.buffer[0:packet_length]
                    packet_crc = packet[-1]

                    cal_crc = crc8_sae_j1850(packet[2:-1])

                    if cal_crc == packet_crc:
                        can_id = (packet[2] << 8) | packet[3]
                        frame_data = bytes(packet[5:-1])

                        frame = CANFrame(can_id, frame_data)
                        frames.append(frame)
                    else: print("CRC ERROR")
                    del self.buffer[:packet_length]

                else:
                    break
            else:
                del self.buffer[0]
                continue

        return frames
