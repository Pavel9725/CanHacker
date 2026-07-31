from app.can_frame import CANFrame
from app.crc import crc8_sae_j1850

START_BYTE_1 = 0x55         # Первый стартовый байт (маркер начала пакета)
START_BYTE_2 = 0xAA         # Второй стартовый байт (маркер начала пакета)


class CANParser:
    """
        Класс для парсинга CAN-пакетов из потока байтов.

        Основные функции:
        1. Принимает поток байтов через метод feed()
        2. Ищет пакеты, начинающиеся с маркеров 0x55 0xAA
        3. Извлекает CAN ID, DLC, данные
        4. Проверяет целостность через CRC-8
        5. Возвращает список извлеченных CANFrame объектов
    """

    def __init__(self):
        self.buffer = bytearray()       # Буфер для накопления входящих данных


    def feed(self, data):
        """
            Обрабатывает входящие данные и извлекает CAN-фреймы.

            Алгоритм работы:
            1. Добавляет новые данные в буфер
            2. Циклически ищет в буфере пакеты, начиная с 0x55 0xAA
            3. Для найденного пакета:
               a. Извлекает DLC (длину данных)
               b. Вычисляет полную длину пакета
               c. Проверяет наличие полного пакета в буфере
               d. Проверяет CRC
               e. Извлекает CAN ID и данные
               f. Создает объект CANFrame
               g. Удаляет обработанный пакет из буфера
            4. Если пакет неполный - прерывает обработку
            5. Если стартовые байты не найдены - удаляет "мусорные" байты

            Возвращает:
                list[CANFrame]: Список успешно извлеченных CAN-фреймов
        """
        self.buffer += data     # Добавляем новые данные в конец буфера
        frames = []             # Список для хранения извлеченных фреймов

        # Ищем начало пакета
        while len(self.buffer)  >= 5:
            if self.buffer[0] == START_BYTE_1 and self.buffer[1] == START_BYTE_2:
                dlc = int(self.buffer[4])

                # Извлекаем полный пакет из буфера
                # Структура: [0x55][0xAA][ID_H][ID_L][DLC][DATA...][CRC]
                packet_length = 2 + 2 + 1 + dlc + 1

                # Проверка наличия полного пакета
                if len(self.buffer) >= packet_length:
                    packet = self.buffer[0:packet_length]           # Извлекаем полный пакет из буфера
                    packet_crc = packet[-1]                         # Последний байт пакета - это CRC

                    cal_crc = crc8_sae_j1850(packet[2:-1])          # Вычисляем CRC для данных

                    # Проверка CRC
                    if cal_crc == packet_crc:
                        can_id = (packet[2] << 8) | packet[3]
                        frame_data = bytes(packet[5:-1])

                        frame = CANFrame(can_id, dlc, frame_data)   # Создаем объект CANFrame
                        frames.append(frame)                        # Добавляем фрейм в список результатов
                    else: print("CRC ERROR")                        # CRC не совпадает - пакет поврежден
                    del self.buffer[:packet_length]                 # Удаляем из буфера обработанный пакет
                else:
                    # Пакет неполный - нужно дождаться новых данных
                    # Прерываем цикл, сохраняя буфер для следующего вызова feed()
                    break
            else:
                # Удаление "мусорных" байтов
                # Если первые байты не являются стартовыми, удаляем их
                del self.buffer[0]
                continue
        return frames
