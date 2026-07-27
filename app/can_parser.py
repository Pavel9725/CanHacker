from can_protocol import CANFrame

class CANParser:

    HEADER = 0xAA

    def __init__(self):
        self.buffer = bytearray()