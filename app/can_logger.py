class CANLogger:

    def __init__(self):
        pass


    def log(self, frame):

        print(
            f"ID: 0x{frame.can_id:X} "
            f"DLC: {frame.dlc} "
            f"DATA: {frame.data.hex(' ')}"
        )