import time


class CANLogger:
    """
       Класс для логирования и отслеживания изменений CAN-сообщений.

       Основные функции:
       1. Хранит последние полученные фреймы по каждому ID
       2. Сравнивает новые фреймы с предыдущими
       3. Фиксирует изменения в данных и DLC
       4. Сохраняет историю всех изменений
   """

    def __init__(self):
        # Словарь для хранения последних фреймов по ID
        self.last_frames = {}

        # Словарь для хранения истории изменений по ID
        self.history = {}


    def log(self, frame):
        """
            Обрабатывает новый CAN-фрейм: логирует изменения и обновляет состояние.

            Алгоритм работы:
            1. Проверяет, был ли уже получен фрейм с таким ID
            2. Если ID новый - выводит информацию о новом сообщении
            3. Если ID уже существует - сравнивает с предыдущим фреймом
            4. Фиксирует изменения в DLC и отдельных байтах данных
            5. Сохраняет изменения в историю
            6. Обновляет последний фрейм для этого ID
    """
        # Получаем предыдущий фрейм с таким ID (или None, если первый раз)
        old_frame = self.last_frames.get(frame.can_id)

        # Если это первый пакет этого ID
        if old_frame is None:
            # Сохраняем новый фрейм как последний для этого ID
            self.last_frames[frame.can_id] = frame

            print(
                f"NEW ID: 0x{frame.can_id:X} "
                f"DATA: {frame.data.hex(' ')}"
            )

            return  # Выходим, так как изменений нет

        # ID уже существует
        # Создаем список для хранения всех изменений
        changes = []

        # Проверяем изменение DLC
        if frame.dlc != old_frame.dlc:
            changes.append(
                {
                    "type": "dlc",              # Тип изменения: DLC
                    "old": old_frame.dlc,       # Старое значение DLC
                    "new": frame.dlc,           # Новое значение DLC
                    "time": time.time()         # Время изменения
                }
            )

        # Определяем максимальную длину для сравнения
        max_length = max(len(old_frame.data), len(frame.data))

        for index in range(max_length):

            old_byte = None                                 # Байт из старого кадра (если есть)
            new_byte = None                                 # Байт из нового кадра (если есть)

            # Получаем байт из старого фрейма, если индекс существует
            if index < len(old_frame.data):
                old_byte = old_frame.data[index]

            # Получаем байт из нового фрейма, если индекс существует
            if index < len(frame.data):
                new_byte = frame.data[index]

            # Если байты отличаются (или один из них None)
            if old_byte != new_byte:
                changes.append(
                    {
                        "type": "byte",             # Тип изменения: байт
                        "index": index,             # Индекс измененного байта
                        "old": old_byte,            # Старое значение (или None)
                        "new": new_byte,            # Новое значение (или None)
                        "time": time.time()         # Время изменения
                    }
                )


        # Если были изменения
        if changes:
            # Если для этого ID еще нет истории - создаем пустой список
            if frame.can_id not in self.history:
                self.history[frame.can_id] = []

            # Добавляем все изменения в историю
            self.history[frame.can_id].extend(changes)

            print(f"ID: 0x{frame.can_id:X} changed:")

            for change in changes:
                # Если изменился байт данных
                if change["type"] == "byte":
                    print(
                        f" byte[{change['index']}]: "
                        f"{change['old']} -> "
                        f"{change['new']}"
                    )

                # Если изменился DLC
                elif change["type"] == "dlc":
                    print(
                        f" DLC: "
                        f"{change['old']} -> "
                        f"{change['new']}"
                    )
        # обновляем последний кадр
        self.last_frames[frame.can_id] = frame