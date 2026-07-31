from app.crc import crc8_sae_j1850

START_BYTE_1 = 0x55         # Первый стартовый байт (маркер начала пакета)
START_BYTE_2 = 0xAA         # Второй стартовый байт (маркер начала пакета)


class CANFrame:
    """
        Класс для представления CAN-фрейма (сообщения).

        Хранит информацию о CAN-сообщении:
        - can_id: 11-битный идентификатор сообщения (0-0x7FF)
        - dlc: длина данных в байтах (Data Length Code, 0-8)
        - data: сами данные в виде байтового массива

        При создании выполняет валидацию входных параметров.
    """

    def __init__(self, can_id: int, dlc: int, data: bytes):
        # Проверяем, что can_id - целое число
        if not isinstance(can_id, int):
            raise TypeError("CAN ID must be int")

        # Проверяем, что dlc - целое число
        if not isinstance(dlc, int):
            raise TypeError("DLC must be int")

        # Проверяем, что data - байтовый массив
        if not isinstance(data, bytes):
            raise TypeError("Data must be bytes")

        # Проверяем соответствие заявленной длины и фактических данных
        # Защита от ошибок: если DLC=8, а данных только 2 байта - ошибка
        if dlc != len(data):
            raise ValueError("DLC does not match DATA length")

        # Сохраняем атрибуты объекта
        self.can_id = can_id
        self.dlc = dlc
        self.data = data



def build_packet(frame: CANFrame) -> bytes:
    """
          Формирует пакет данных для отправки по последовательному интерфейсу.

          Структура пакета:
          [0x55][0xAA][CAN ID 2 байта][DLC 1 байт][Данные][CRC 1 байт]

          Алгоритм:
          1. Добавляет стартовые байты (0x55, 0xAA) для синхронизации
          2. Добавляет 11-битный CAN ID (упакованный в 2 байта, big-endian)
          3. Добавляет DLC (длину данных)
          4. Добавляет сами данные
          5. Рассчитывает CRC-8 для всех байтов от ID до данных включительно
          6. Добавляет CRC в конец пакета
  """

    # Создаем изменяемый байтовый массив для сборки пакета
    packet = bytearray()

    # Добавляем стартовые байты (маркеры начала пакета)
    packet.append(START_BYTE_1)
    packet.append(START_BYTE_2)

    # Добавляем CAN ID (11 бит) в виде 2 байт (старший байт первым)
    packet.extend(frame.can_id.to_bytes(2, byteorder='big'))

    # Добавляем DLC (длину данных) - 1 байт
    packet.append(frame.dlc)

    # Добавляем сами данные (от 0 до 8 байт)
    packet.extend(frame.data)

    # Рассчитываем CRC-8 по алгоритму SAE J1850. CRC считается для всех байтов, начиная с ID (после стартовых байтов)
    # То есть для: [CAN_ID 2 байта][DLC][Данные]
    crc_data = packet[2:]
    crc = crc8_sae_j1850(crc_data)

    # Добавляем CRC в конец пакета
    packet.append(crc)

    # Возвращаем пакет как неизменяемый байтовый объект
    return bytes(packet)

