from app.serial_manager import SerialManager
import serial


def test_serial_connect_success(mocker):
    manager = SerialManager()
    fake_serial = mocker.Mock()

    mocker.patch("serial.Serial", return_value=fake_serial)
    result = manager.connect("COM3", 115200, 1)

    assert result is True
    assert manager.is_connected() is True


def test_serial_connect_fail(mocker):
    manager = SerialManager()

    mocker.patch("serial.Serial", side_effect=serial.SerialException)
    result = manager.connect("COM99", 115200, 1)

    assert result is False
    assert manager.is_connected() is False


def test_serial_disconnect(mocker):
    manager = SerialManager()
    fake_serial = mocker.Mock()

    mocker.patch("serial.Serial", return_value=fake_serial)
    manager.connect("COM3", 115200, 1)
    result = manager.disconnect()

    assert result is True

    fake_serial.close.assert_called_once()