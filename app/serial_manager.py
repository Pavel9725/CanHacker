from datetime import datetime
import serial.tools.list_ports
import serial


class SerialManager:
    """
        Менеджер для работы с последовательным портом (UART/COM).

        Основные функции:
        1. Поиск доступных портов
        2. Подключение к порту с заданными параметрами
        3. Чтение и запись данных
        4. Очистка буферов
        5. Диагностика и обработка ошибок
        6. Информация о подключении
    """
    def __init__(self):
        self._serial = None                     # Основной объект для работы с последовательным портом

        # Параметры подключения
        self._port = None                       # Имя порта (например, COM3)
        self._baudrate = None                   # Скорость передачи (bps)
        self._timeout = 0                       # Таймаут в секундах (0 - non-blocking)

        self._bytesize = serial.EIGHTBITS       # 8 бит данных
        self._parity = serial.PARITY_NONE       # Нет контроля четности
        self._stopbits = serial.STOPBITS_ONE    # 1 стоп-бит

        #Diagnostics
        self._last_error = None                 # Последняя ошибка
        self._connect_time = None               # Время подключения

    def get_ports(self) -> list:
        """
            Возвращает список доступных последовательных портов.

            Получает информацию обо всех доступных COM-портах/устройствах
            с их описанием и аппаратным идентификатором.
        """
        # Получаем список всех доступных портов
        ports = serial.tools.list_ports.comports()
        ports_data = []

        # Преобразуем каждый порт в словарь с нужной информацией
        for port in ports:
            ports_data.append(
                {
                    'device': port.device,              # Имя устройств
                    'description': port.description,    # Описание порта
                    'hwid': port.hwid                   # Аппаратный ID
                }
            )
        return ports_data


    def _reset_connection(self):
        """
           Сбрасывает все параметры подключения (внутренний метод).

           Используется для очистки состояния после отключения или ошибки.
           Возвращает объект в начальное состояние.
       """
        self._serial = None

        self._port = None
        self._baudrate = None
        self._timeout = 1

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
            self._last_error = None                     # Очищаем предыдущую ошибку перед подключением

            # Если уже подключены, отключаемся
            if self.is_connected():
                self.disconnect()

            # Создаем объект Serial с заданными параметрами
            self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout,
                                         bytesize=bytesize, parity=parity, stopbits=stopbits)

            # Проверяем, что порт успешно открыт
            if not self._serial.is_open:
                raise serial.SerialException("Не удалось открыть порт.")

            # Удаляем все накопленные данные, чтобы начать с чистого состояния
            self._serial.reset_input_buffer()
            self._serial.reset_output_buffer()

            # Сохраняем параметры подключения
            self._port = port
            self._baudrate = baudrate
            self._timeout = timeout
            self._bytesize = bytesize
            self._parity = parity
            self._stopbits = stopbits
            self._connect_time = datetime.now()

            return True

        # Обработка ошибки ValueError (неверные параметры)
        except ValueError as ve:
            if self.is_connected():
                self._serial.close()
            self._reset_connection()
            self._last_error = str(ve)
            return False

        # Обработка ошибки SerialException (проблемы с портом)
        except serial.SerialException as se:
            if self.is_connected():
                self._serial.close()
            self._reset_connection()
            self._last_error = str(se)
            return False

        # Обработка всех остальных исключений
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
            # Если порт открыт - закрываем его
            if self.is_connected():
                self._serial.close()

            # Сбрасываем состояние
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
        """
           Очищает входной буфер (принятые, но не прочитанные данные).
           Используется для сброса старых данных перед началом нового сеанса.
        """
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
