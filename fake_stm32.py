import serial
import time


PORT = "COM7"
BAUDRATE = 115200


ser = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    timeout=0
)


print("Fake STM32 started")
print("Port:", PORT)


counter = 0


while True:

    # Проверяем входящие данные
    if ser.in_waiting:

        data = ser.read(ser.in_waiting)

        print("RX:", data)

        # Ответ как будто STM32
        response = b"ACK:" + data

        ser.write(response)


    # Периодическая отправка данных
    counter += 1

    if counter >= 500:
        ser.write(b"CAN:0x7E8:8:0509000024230000")
        counter = 0


    time.sleep(0.001)