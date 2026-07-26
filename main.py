from serial_manager import SerialManager

manager = SerialManager()
ports = manager.get_ports()

if not ports:
    print("Нет доступных COM-портов!")
    raise SystemExit
else:
    print("\nДоступные порты:")
    for index, port in enumerate(ports, start=1):
        print(f"{index}. {port['device']} - {port['description']}")

selected_baudrate = 115200
selected_timeout = 1

while True:
    try:
        selected_port = input("Введите номер порта: ")
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


connected = manager.connect(selected_port['device'], selected_baudrate, selected_timeout)
if connected and manager.is_connected():
    try:
        print("Подключение успешно!")
        print(f"Порт: {selected_port['device']}\nСкорость: {selected_baudrate}\n")

        input("Нажмите Enter для отключения...\n")

    except KeyboardInterrupt:
        print("⚠️ Прервано пользователем\n")

    except Exception as e:
        print(f"Ошибка во время работы с портом {e}")
    finally:
        if manager.disconnect():
            print("Отключено!")
        else:
            print("Ошибка отключения!")

else:
    print("Ошибка подключения!")





