import time

from serial_manager import SerialManager
from can_receiver import CANReceiver
from can_dispatcher import CANDispatcher
from can_model import CANModel
from can_logger import CANLogger


def select_port(ports):
    print("\nДоступные порты:")

    for index, port in enumerate(ports, start=1):
        print(
            f"{index}. "
            f"{port['device']} - "
            f"{port['description']}"
        )

    while True:

        try:
            selected = input("Выберите номер порта: ")

            if selected == "":
                print("Введите номер")
                continue

            index = int(selected) - 1

            if 0 <= index < len(ports):
                return ports[index]

            print(
                f"Введите число от 1 до {len(ports)}"
            )

        except ValueError:
            print("Это не число! Попробуйте снова.")


def main():


    manager = SerialManager()

    receiver = CANReceiver(manager)

    model = CANModel()
    logger = CANLogger()

    dispatcher = CANDispatcher(
        receiver.queue
    )

    ports = manager.get_ports()

    if not ports:
        print("Нет доступных COM-портов!")
        return


    selected_port = select_port(ports)

    selected_baudrate = 115200



    connected = manager.connect(
        selected_port["device"],
        selected_baudrate
    )

    if not (connected and manager.is_connected()):

        print("Ошибка подключения!")
        print(manager.get_last_error())

        return


    dispatcher.add_listeners([
        model,
        logger,
    ])


    try:

        print("\nПодключение успешно!")

        info = manager.get_connection_info()
        print(info)

        print("\nОжидание CAN пакетов...")
        print("Ctrl+C - выход\n")

        receiver.start()
        dispatcher.start()

        while True:

            time.sleep(0.1)


    except KeyboardInterrupt:
        print("\nОстановка пользователем.")

    except Exception as e:
        print(f"Ошибка во время работы: {e}")
    finally:
        print("Остановка компонентов...")

        dispatcher.stop()
        receiver.stop()

        if manager.disconnect():
            print("Порт закрыт.")
        else:
            print("Ошибка отключения.")


if __name__ == "__main__":
    main()
