import time
from queue import Queue

from app.can_dispatcher import CANDispatcher
from app.can_frame import CANFrame
from app.can_logger import CANLogger


def test_dispatcher_sends_frame_to_logger():
    queue = Queue()

    dispatcher = CANDispatcher(queue)
    logger = CANLogger()

    dispatcher.add_listener(logger)

    frame = CANFrame(0x7E8, 3, bytes([1, 2, 3]))
    queue.put(frame)
    dispatcher.start()
    deadline = time.time() + 1

    while 0x7E8 not in logger.last_frames:
        if time.time() >= deadline:
            break

        time.sleep(0.01)

    dispatcher.stop()

    assert 0x7E8 in logger.last_frames
    assert logger.last_frames[0x7E8] is frame

