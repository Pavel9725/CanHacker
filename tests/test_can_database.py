from app.can_database import CANDatabase
from app.can_frame import CANFrame
import time


def test_database_add_new_frame():
    db = CANDatabase() #Создаем пустую базу данных

    frame = CANFrame(0x7E8, 3, bytes([1,2,3])) #Создаем тестовый CAN кадр

    db.update(frame) #Добавляем кадр в базу

    data = list(db.get_all()) #Получаем все сохраненные данные

    assert len(data) == 1 #Проверяем что в базе ровно одна запись

    assert data[0]["frame"].can_id == 0x7E8 #Проверяем что ID кадра сохранен правильно

    assert data[0]["count"] == 1 #Проверяем, что счетчик сообщений равен 1 (первое получение)


def test_database_update_existing_id():
    db = CANDatabase()

    # Создаем два фрейма с одинаковым ID, но разными данными
    frame1 = CANFrame(0x7E8, 3, bytes([1, 2, 3]))
    frame2 = CANFrame(0x7E8, 3, bytes([4, 5, 6]))

    db.update(frame1)   # Добавляем кадр в базу
    db.update(frame2)   # Добавляем тот же кадр в базу

    data = list(db.get_all())

    assert len(data) == 1                               # Проверяем, что запись осталась одна (данные обновились, а не добавились)
    assert data[0]['count'] == 2                        # Счетчик должен увеличиться до 2
    assert data[0]['frame'].data == bytes([4, 5, 6])    # Данные должны обновиться на последние (frame2)


def test_database_multiple_ids():
    db = CANDatabase()

    frame1 = CANFrame(0x7E8, 3, bytes([1, 2, 3]))
    frame2 = CANFrame(0x7E9, 3, bytes([0xAA, 0xBB, 0xCC]))

    db.update(frame1)
    db.update(frame2)

    data = list(db.get_all())

    assert len(data) == 2                                       # Должно быть две разные записи (по одной на каждый ID)

    # Проверяем данные первого фрейма
    assert data[0]['count'] == 1
    assert data[0]['frame'].data == bytes([1, 2, 3])

    # Проверяем данные второго фрейма
    assert data[1]['count'] == 1
    assert data[1]['frame'].data == bytes([0xAA, 0xBB, 0xCC])

def test_database_count_messages():
    db = CANDatabase()

    frame = CANFrame(0x7E8, 3, bytes([1, 2, 3]))

    # Отправляем одно и то же сообщение 4 раза
    db.update(frame)
    db.update(frame)
    db.update(frame)
    db.update(frame)

    data = list(db.get_all())

    # Должна быть одна запись (один ID)
    assert len(data) == 1

    # Счетчик должен быть равен 4
    assert data[0]["count"] == 4


def test_database_time_tracking():
    db = CANDatabase()

    frame = CANFrame(0x7E8, 2, bytes([1,2]))

    before = time.time()            # Запоминаем время ДО добавления
    db.update(frame)                # Добавляем фрейм
    after = time.time()             # Запоминаем время ПОСЛЕ добавления


    data = list(db.get_all())[0]    # Получаем сохраненные данные

    # Проверяем, что время первого получения находится между before и after
    assert before <= data["first_seen"] <= after

    # Проверяем, что время последнего получения тоже в этом диапазоне
    assert before <= data["last_seen"] <= after


def test_database_last_seen_updates():
    db = CANDatabase()

    frame = CANFrame(0x7E8, 2, bytes([1,2]))

    db.update(frame)
    item1 = list(db.get_all())[0]
    first_time = item1["first_seen"]    # Время первого получения
    last_time_1 = item1["last_seen"]    # Время последнего получения (пока равно first_time)

    time.sleep(0.01)                    # Ждем 10 миллисекунд

    db.update(frame)                     # Второе получение того же ID
    item2 = list(db.get_all())[0]

    # Время первого получения НЕ должно измениться
    assert item2["first_seen"] == first_time

    # Время последнего получения ДОЛЖНО увеличиться
    assert item2["last_seen"] > last_time_1
