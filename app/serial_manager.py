from datetime import datetime

import serial.tools.list_ports
import serial



class SerialManager:

    def __init__(self):
        self._serial = None

        #Connection parameters
        self._port = None
        self._baudrate = None
        self._timeout = 0

        self._bytesize = serial.EIGHTBITS
        self._parity = serial.PARITY_NONE
        self._stopbits = serial.STOPBITS_ONE

        #Diagnostics
        self._last_error = None
        self._connect_time = None

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
        self._timeout = 0

        self._bytesize = serial.EIGHTBITS
        self._parity = serial.PARITY_NONE
        self._stopbits = serial.STOPBITS_ONE

        self._connect_time = None


    def connect(self,


                port: str,
                baudrate: int,
                timeout: float = 0,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                ) -> bool:



        try:
            self._last_error = None                     #Clear error before connection

            if self.is_connected():
                self.disconnect()

            self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout,
                                         bytesize=bytesize, parity=parity, stopbits=stopbits)

            if not self._serial.is_open:
                raise serial.SerialException("Не удалось открыть порт.")

            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()

            self._port = port
            self._baudrate = baudrate
            self._timeout = timeout
            self._bytesize = bytesize
            self._parity = parity
            self._stopbits = stopbits
            self._connect_time = datetime.now()

            return True

        except ValueError as ve:
            if self.is_connected():
                self._serial.close()
            self._reset_connection()
            self._last_error = str(ve)
            return False

        except serial.SerialException as se:
            if self.is_connected():
                self._serial.close()
            self._reset_connection()
            self._last_error = str(se)
            return False

        except Exception as e:
            if self.is_connected():
                self._serial.close()
            self._reset_connection()
            self._last_error = str(e)
            return False

    def is_connected(self) -> bool:
        return bool(self._serial and self._serial.is_open)

    def get_last_error(self) -> str | None:
        return self._last_error


    def disconnect(self) -> bool:

        try:
            if self.is_connected():
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


    def flush_input(self) -> bool:
        try:
            if not self.is_connected():
                self._last_error = "Порт не подключен."
                return False

            self._serial.reset_input_buffer()
            self._last_error = None
            return True

        except serial.SerialException as se:
            self._last_error = str(se)
            return False

        except Exception as e:
            self._last_error = str(e)
            return False

    def flush_output(self) -> bool:
        try:
            if not self.is_connected():
                self._last_error = "Порт не подключен."
                return False

            self._serial.reset_output_buffer()
            self._last_error = None
            return True

        except serial.SerialException as se:
            self._last_error = str(se)
            return False

        except Exception as e:
            self._last_error = str(e)
            return False


    def read(self, length: int = 0) -> bytes | None:
        try:
            if not self.is_connected():
                self._last_error = 'Порт не подключен.'
                return None

            if length > 0:
                data = self._serial.read(length)
            else:
                count = self._serial.in_waiting

                if count > 0:
                    data = self._serial.read(count)
                else:
                    data = b''

            self._last_error = None
            return data

        except serial.SerialException as se:
            self._last_error = str(se)
            return None

        except Exception as e:
            self._last_error = str(e)
            return None




    def write(self, data: bytes) -> bool:
        try:
            if not self.is_connected():
                self._last_error = 'Порт не подключен.'
                return False

            if not isinstance(data, bytes):
                self._last_error = "Данные должны быть bytes."
                return False

            written = self._serial.write(data)

            if written != len(data):
                self._last_error = "Не все данные отправлены."
                return False

            self._last_error = None
            return True

        except serial.SerialException as se:
            self._last_error = str(se)
            return False

        except Exception as e:
            self._last_error = str(e)
            return False


    def get_connection_info(self) -> dict:
        return {
            'connected': self.is_connected(),
            'port': self._port,
            'baudrate': self._baudrate,
            'timeout': self._timeout,
            'connect_time': self._connect_time
        }

    def clear_error(self):
        self._last_error = None
