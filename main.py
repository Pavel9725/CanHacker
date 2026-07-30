from can_logger import CANLogger
from serial_manager import SerialManager
from can_parser import CANParser
from can_database import CANDatabase


manager = SerialManager()
parser = CANParser()
logger = CANLogger()
database = CANDatabase()

ports = manager.get_ports()


if not ports:
    print("Нет доступных COM-портов!")
    raise SystemExit


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


connected = manager.connect(
    selected_port['device'],
    selected_baudrate
)


if not (connected and manager.is_connected()):
    print("Ошибка подключения!")
    print(manager.get_last_error())
    raise SystemExit



try:
    print("\nПодключение успешно!")

    info = manager.get_connection_info()
    print(info)

    print("\nОжидание CAN пакетов...")
    print("Ctrl+C - выход\n")


    while True:

        data = manager.read()

        if data:

            frames = parser.feed(data)

            for frame in frames:
                database.update(frame)
                logger.log(frame)

            print("\n--- CAN DATABASE ---")

            for item in database.get_all():
                frame = item["frame"]

                print(
                    f"0x{frame.can_id:X} "
                    f"{frame.data.hex(' ')} "
                    f"count={item['count']}"
                )







except KeyboardInterrupt:
    print("\nОстановка пользователем.")


except Exception as e:
    print(f"Ошибка во время работы: {e}")


finally:

    if manager.disconnect():
        print("Порт закрыт.")
    else:
        print("Ошибка отключения.")