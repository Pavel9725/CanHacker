import time
from queue import Queue

from app.can_dispatcher import CANDispatcher
from app.can_frame import CANFrame


class FakeListener:

    def __init__(self):
        self.received_frames = []

    def handle_frame(self, frame):
        self.received_frames.append(frame)


def test_dispatcher_add_listener():
    queue = Queue()
    dispatcher = CANDispatcher(queue)

    listener = FakeListener()

    dispatcher.add_listener(listener)

    assert listener in dispatcher.listeners


def test_dispatcher_add_listeners():
    queue = Queue()
    dispatcher = CANDispatcher(queue)

    listener1 = FakeListener()
    listener2 = FakeListener()

    dispatcher.add_listeners([listener1, listener2])

    assert listener1 in dispatcher.listeners
    assert listener2 in dispatcher.listeners
    assert len(dispatcher.listeners) == 2


def test_dispatcher_remove_listener():
    queue = Queue()
    dispatcher = CANDispatcher(queue)

    listener = FakeListener()

    dispatcher.add_listener(listener)
    dispatcher.remove_listener(listener)

    assert listener not in dispatcher.listeners


def test_dispatcher_passes_frame_to_listener():
    queue = Queue()
    dispatcher = CANDispatcher(queue)

    listener = FakeListener()
    dispatcher.add_listener(listener)

    frame = CANFrame(0x7E8, 3, bytes([1, 2, 3]))
    queue.put(frame)
    dispatcher.start()
    deadline = time.time() + 1

    while not listener.received_frames:
        if time.time() >= deadline:
            break
        time.sleep(0.01)

    dispatcher.stop()

    assert len(listener.received_frames) == 1
    assert listener.received_frames[0] is frame


def test_dispatcher_passes_frame_to_all_listeners():
    queue = Queue()
    dispatcher = CANDispatcher(queue)

    listener1 = FakeListener()
    listener2 = FakeListener()

    dispatcher.add_listeners([listener1, listener2])

    frame = CANFrame(0x7E8, 3, bytes([1, 2, 3]))

    queue.put(frame)

    dispatcher.start()

    deadline = time.time() + 1

    while (
        not listener1.received_frames
        or not listener2.received_frames
    ):
        if time.time() >= deadline:
            break
        time.sleep(0.01)

    dispatcher.stop()

    assert listener1.received_frames[0] is frame
    assert listener2.received_frames[0] is frame


def test_dispatcher_start():
    queue = Queue()
    dispatcher = CANDispatcher(queue)

    dispatcher.start()

    assert dispatcher.running is True
    assert dispatcher.thread is not None
    assert dispatcher.thread.is_alive()

    dispatcher.stop()


def test_dispatcher_stop():
    queue = Queue()
    dispatcher = CANDispatcher(queue)

    dispatcher.start()
    dispatcher.stop()

    assert dispatcher.running is False
    assert dispatcher.thread is None


def test_dispatcher_start_twice():
    queue = Queue()
    dispatcher = CANDispatcher(queue)

    dispatcher.start()

    first_thread = dispatcher.thread

    dispatcher.start()

    assert dispatcher.thread is first_thread

    dispatcher.stop()


def test_dispatcher_empty_queue_does_not_crash():
    queue = Queue()
    dispatcher = CANDispatcher(queue)

    dispatcher.start()

    time.sleep(0.2)

    assert dispatcher.thread.is_alive()

    dispatcher.stop()

    assert dispatcher.thread is None

