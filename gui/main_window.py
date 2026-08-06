from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox

from serial_manager import SerialManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CAN Hacker")
        self.resize(800, 600)
        self.setMinimumSize(400, 400)


        self.serial_manager = SerialManager()
        self.port_combo = QComboBox()

        self.button = QPushButton("Подключиться")
        self.button.clicked.connect(self.connect_to_port)





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
        connection_layout.addWidget(self.button)
        layout.addLayout(connection_layout)

        self.refresh_ports()




    def connect_to_port(self):
        selected_port = self.port_combo.currentText()
        print(selected_port)

    def refresh_ports(self):
        self.port_combo.clear()
        ports = self.serial_manager.get_ports()

        ports_device = []
        for port in ports:
            ports_device.append(port['device'])

        self.port_combo.addItems(ports_device)



