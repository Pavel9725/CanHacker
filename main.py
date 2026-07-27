from serial_manager import SerialManager
import time

manager = SerialManager()
ports = manager.get_ports()

if not ports:
    print("Нет доступных COM-портов!")
    raise SystemExit
else:
    print("\nДоступные порты:")
    for index, port in enumerate(ports, start=1):
        print(f"{index}. {port['device']} - {port['description']}")

while True:
    try:
        selected_port = input("Выберите номер порта: ")
        if selected_port == "":
            print("Введите номер")
            continue

        index = int(selected_port) - 1

        if 0 <= index < len(ports):
            selected_port = ports[index]
            break
        else:
            print(f"Введите число от 1 до {len(ports)}")

    except ValueError:
        print("Это не число! Попробуйте снова.")

selected_baudrate = 115200


connected = manager.connect(selected_port['device'], selected_baudrate)

if connected and manager.is_connected():
    try:
        print("Подключение успешно!")

        info = manager.get_connection_info()
        print(info)

        manager.write(b"PING")

    except KeyboardInterrupt:
        print("⚠️ Прервано пользователем\n")

    except Exception as e:
        print(f"Ошибка во время работы с портом {e}")


else:
    print("Ошибка подключения!")
    print(manager.get_last_error())
    exit()

try:

    print("Ожидание данных...\n")
    print("Ctrl+C - выход\n")

    while True:

        data = manager.read()

        if data:
            print("Получено:")
            print("RAW:", data)
            print("HEX:", data.hex(' '))
            print("LEN:", len(data))

        time.sleep(0.01)


except KeyboardInterrupt:
    print("Остановка пользователем.\n")


finally:

    if manager.disconnect():
        print("Порт закрыт.")
    else:
        print("Ошибка отключения.")





