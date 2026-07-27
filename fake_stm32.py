import serial
import time


PORT = "COM7"
BAUDRATE = 115200

can_id = 0x7E8
packet = bytes([
    0xAA,       # header

   *can_id.to_bytes(2, byteorder='big'),

    0x08,       # DLC

    0x11,
    0x22,
    0x33,
    0x44,
    0x55,
    0x66,
    0x77,
    0x88
])



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

    if counter >= 1000:
        ser.write(packet)
        counter = 0


    time.sleep(0.001)