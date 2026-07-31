from app.can_receiver import CANReceiver
from app.can_frame import CANFrame, build_packet
import time


def test_receiver_thread_receive_frame(mocker):
    fake_serial = mocker.Mock()
    frame = CANFrame(0x7E8, 3, bytes([1, 2, 3]))
    packet = build_packet(frame)

    fake_serial.read.side_effect = [
        packet,
        b""
    ]

    receiver = CANReceiver(fake_serial)
    receiver.start()

    result = receiver.queue.get(timeout=1)

    assert result.can_id == 0x7E8
    assert result.data ==  bytes([1, 2, 3])

    receiver.stop()

def test_receiver_stop(mocker):
    fake_serial = mocker.Mock()
    fake_serial.read.return_value = b""

    receiver = CANReceiver(fake_serial)
    receiver.start()

    time.sleep(0.05)

    assert receiver.thread.is_alive()

    receiver.stop()

    assert receiver.thread is None