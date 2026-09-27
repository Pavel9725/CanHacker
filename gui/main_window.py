from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from PySide6.QtCore import QTimer

from serial_manager import SerialManager

from app.can_model import CANModel
from app.can_dispatcher import CANDispatcher
from app.can_receiver import CANReceiver


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("CAN Hacker")
        self.resize(800, 600)
        self.setMinimumSize(400, 400)


        self.serial_manager = SerialManager()
        self.can_receiver = CANReceiver(self.serial_manager)
        self.can_model = CANModel()
        self.can_dispatcher = CANDispatcher(self.can_receiver.queue)
        self.can_dispatcher.add_listener(self.can_model)

        self.port_combo = QComboBox()
        self.known_ports = []

        self.status_indicator = QLabel()
        self.status_indicator.setText("●")

        self.port_timer = QTimer()
        self.port_timer.timeout.connect(self.refresh_ports)
        self.port_timer.start(500)

        self.button = QPushButton("Подключиться")
        self.button.clicked.connect(self.toggle_connection)


        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        label = QLabel("Can Hacker")
        label_2 = QLabel("Serial CAN Monitor")
        layout.addWidget(label)
        layout.addWidget(label_2)

        connection_layout = QHBoxLayout()
        port_label = QLabel("Port:")





        connection_layout.addWidget(port_label)
        connection_layout.addWidget(self.port_combo)
        connection_layout.addWidget(self.status_indicator)
        connection_layout.addWidget(self.button)
        layout.addLayout(connection_layout)

        self.refresh_ports()




    def connect_to_port(self):
        selected_port = self.port_combo.currentText()
        connected = self.serial_manager.connect(selected_port, 115200)
        
        if connected:
            self.can_receiver.start()
            self.can_dispatcher.start()

            print("Порт подключен.")
            self.status_indicator.setStyleSheet("color: green;")
            self.button.setText("Отключиться")

        else:
            print(self.serial_manager.get_last_error())
            self.status_indicator.setStyleSheet("color: red;")
            self.button.setText("Подключиться")


    def disconnect_from_port(self):
        self.can_receiver.stop()
        self.can_dispatcher.stop()

        self.serial_manager.disconnect()

        self.status_indicator.setStyleSheet("color: red;")
        self.button.setText("Подключиться")

    def refresh_ports(self):
        ports = self.serial_manager.get_ports()
        connection_info = self.serial_manager.get_connection_info()

        ports_device = []

        for port in ports:
            ports_device.append(port['device'])

        if connection_info['connected']:
            connected_port = connection_info['port']

            if connected_port not in ports_device:
                self.disconnect_from_port()
                return

        if ports_device == self.known_ports:
            return

        current_port = self.port_combo.currentText()
        self.known_ports = ports_device

        self.port_combo.clear()
        self.port_combo.addItems(ports_device)

        index = self.port_combo.findText(current_port)

        if index >= 0:
            self.port_combo.setCurrentIndex(index)


    def toggle_connection(self):
        if self.serial_manager.is_connected():
            self.disconnect_from_port()
        else:
            self.connect_to_port()



