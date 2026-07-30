import time


class CANLogger:

    def __init__(self):
        # последние кадры по ID
        self.last_frames = {}

        # история изменений
        self.history = {}


    def log(self, frame):

        old_frame = self.last_frames.get(frame.can_id)


        # если это первый пакет этого ID
        if old_frame is None:

            self.last_frames[frame.can_id] = frame

            print(
                f"NEW ID: 0x{frame.can_id:X} "
                f"DATA: {frame.data.hex(' ')}"
            )

            return


        changes = []


        # сравниваем байты
        for index, new_byte in enumerate(frame.data):

            old_byte = old_frame.data[index]


            if old_byte != new_byte:

                change = {
                    "index": index,
                    "old": old_byte,
                    "new": new_byte,
                    "time": time.time()
                }

                changes.append(change)


        # если были изменения
        if changes:

            if frame.can_id not in self.history:
                self.history[frame.can_id] = []


            self.history[frame.can_id].extend(changes)


            print(
                f"ID: 0x{frame.can_id:X} changed:"
            )


            for c in changes:

                print(
                    f" byte[{c['index']}]: "
                    f"{c['old']:02X} -> "
                    f"{c['new']:02X}"
                )


        # обновляем последний кадр
        self.last_frames[frame.can_id] = frame