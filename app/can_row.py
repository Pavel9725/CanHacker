from app.byte_state import ByteState


class CANRow:

    def __init__(self, frame):

        self.can_id = frame.can_id
        self.dlc = frame.dlc

        self.bytes = [ByteState(value) for value in frame.data]


    def update(self, frame):
        self.dlc = frame.dlc

        for index, new_value in enumerate(frame.data):

            if index >= len(self.bytes):

                self.bytes.append(ByteState(new_value))
                continue

            byte_state = self.bytes[index]

            byte_state.update(new_value)


    def get_data(self):
        return [byte.value for byte in self.bytes[:self.dlc]]


    def get_changed_bytes(self):
        changed = []

        for index, byte in enumerate(self.bytes[:self.dlc]):

            if byte.is_changed():
                changed.append(index)

        return changed


    def get_byte(self, index):
        if index < 0 or index >= self.dlc:
            return None

        return self.bytes[index].value


    def is_byte_changed(self, index):
        if index < 0 or index >= self.dlc:
            return False

        return self.bytes[index].is_changed()
