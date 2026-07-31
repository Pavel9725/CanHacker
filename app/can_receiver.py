import time
from queue import Queue, Full
from app.can_parser import CANParser
import threading


class CANReceiver:

    def __init__(self, serial_manager):
        self.serial = serial_manager
        self.parser = CANParser()
        self.queue = Queue(maxsize=1000000)
        self.thread = None
        self.running = False
        self.lost_frames = 0
        self.THREAD_STOP_TIMEOUT = 2

    def _worker(self):
        while self.running:
            data = self.serial.read()

            if data:
                frames = self.parser.feed(data)
                for frame in frames:
                    try:
                        self.queue.put_nowait(frame)
                    except Full:
                        self.lost_frames += 1
            else:
                time.sleep(0.01)
                continue


    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.running = True
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()


    def stop(self):
        self.running = False

        if self.thread:
            self.thread.join(timeout=self.THREAD_STOP_TIMEOUT)

            if self.thread.is_alive():
                print("Warning: receiver thread did not stop")

        self.thread = None

