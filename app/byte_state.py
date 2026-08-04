import time


class ByteState:

    CHANGE_DISPLAY_TIME = 1.0

    def __init__(self, value):
        self.value = value
        self.changed_at = None

    def update(self, value):
        if self.value == value:
            return False

        self.value = value
        self.changed_at = time.time()

        return True

    def is_changed(self):
        if self.changed_at is None:
            return False

        return (time.time() - self.changed_at < self.CHANGE_DISPLAY_TIME)
