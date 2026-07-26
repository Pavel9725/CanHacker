import serial.tools.list_ports
import serial


class SerialManager:

    def __init__(self):
        self._serial = None
        self._port = None
        self._baudrate = None
        self._timeout = 1
        self._connected = False
        self._last_error = None


    def get_ports(self) -> list:
        ports = serial.tools.list_ports.comports()
        ports_data = []

        for port in ports:
            ports_data.append(
                {
                    'device': port.device,
                    'description': port.description,
                    'hwid': port.hwid
                }
            )

        return ports_data

    def _reset_connection(self):
        self._serial = None
        self._port = None
        self._baudrate = None
        self._connected = False
        self._timeout = 1

    def connect(self, port, baudrate, timeout) -> bool:
        try:
            self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
            self._port = port
            self._baudrate = baudrate
            self._timeout = timeout
            self._connected = True
            self._last_error = None

            return True

        except ValueError as ve:
            self._reset_connection()
            self._last_error = str(ve)
            return False

        except serial.SerialException as se:
            self._reset_connection()
            self._last_error = str(se)
            return False

        except Exception as e:
            self._reset_connection()
            self._last_error = str(e)
            return False

    def is_connected(self) -> bool:
        return bool(self._serial and self._serial.is_open and self._connected)


    def disconnect(self) -> bool:

        try:
            if self._serial and self._serial.is_open:
                self._serial.close()

            self._reset_connection()
            self._last_error = None
            return True

        except serial.SerialException as se:
            self._last_error = str(se)
            self._reset_connection()
            return False

        except Exception as e:
            self._last_error = str(e)
            self._reset_connection()
            return False

