################################################################################
# GUI Python File
#
#
#
################################################################################
import sys

from PySide6 import QtCore, QtWidgets, QtGui

import serial.tools.list_ports

# Gui Imports
from App.panel.main_tab_panel import MainTabPanel


from App.Data_Collector import DataCollectorThread, CollectorStatus
import App.Settings_Interface
from App.Settings_Interface import ParamDef


__VERSION__ = "v1.0"


class Gui(QtWidgets.QMainWindow):
    status_signal = QtCore.Signal(int)
    settings_signal = QtCore.Signal(str)

    def __init__(self):
        super(Gui, self).__init__()

        # Initilise settings and data storage
        self.param_defs: list[ParamDef] = App.Settings_Interface.load()
        App.Settings_Interface.set_param_defs(self.param_defs)
        self.serial_port = None
        
        self.nbr_data_points = len(self.param_defs) + 1  # Plus one to include time
        self.data = [[] for _ in range(self.nbr_data_points)]

        # Initilise GUI
        self.setWindowTitle(f"FS DAQ Monitoring - {__VERSION__}")
        self.init_threads()
        self.init_tool_bar()
        self.tab_panel = MainTabPanel(self.param_defs)
        self.setCentralWidget(self.tab_panel)
        self.showMaximized()

    def init_threads(self):
        data_collection_thread = DataCollectorThread(self, self.param_defs)
        self.status_signal.connect(data_collection_thread.status_signal_slot)
        self.settings_signal.connect(data_collection_thread.settings_signal_slot)
        data_collection_thread.data_signal.connect(self.received_data)
        data_collection_thread.start()

    def init_tool_bar(self):
        tool_bar = QtWidgets.QToolBar()
        self.addToolBar(tool_bar)

        stop_btn = QtGui.QAction("Stop", self)
        stop_btn.triggered.connect(self.on_stop_monitoring)
        tool_bar.addAction(stop_btn)

        start_btn = QtGui.QAction("Start", self)
        start_btn.triggered.connect(self.on_start_monitoring)
        tool_bar.addAction(start_btn)

        serial_port_label = QtWidgets.QLabel()
        serial_port_label.setText("Serial Port: ")
        tool_bar.addWidget(serial_port_label)

        self.serial_port_selector = QtWidgets.QComboBox()
        self.serial_port_selector.view().pressed.connect(self.populate_serial_combo)
        self.serial_port_selector.currentTextChanged.connect(self.set_serial_port)

        self.populate_serial_combo()

        tool_bar.addWidget(self.serial_port_selector)

    def populate_serial_combo(self):
        self.serial_port_selector.clear()
        for port, description, _ in sorted(serial.tools.list_ports.comports()):
            self.serial_port_selector.addItem(f"{port} - {description}")

    def set_serial_port(self):
        print("Changing serial port")
        port, desc = str(self.serial_port_selector.currentText()).split(" - ")
        self.settings_signal.emit(port)

    def on_start_monitoring(self):
        print("Starting monitoring")
        self.status_signal.emit(CollectorStatus.RUNNING)

    def on_stop_monitoring(self):
        print("Stopping monitoring")
        self.status_signal.emit(CollectorStatus.STOPPED)

    @QtCore.Slot(object)
    def received_data(self, input_data):
        """Qt Slot to receive all data received from DataCollector
        :param input_data: lis(str): processed data received from signal slot
        """
        # Store data
        for i in range(self.nbr_data_points):
            self.data[i].append(input_data[i])

        # Trigger update of data for tab panel
        self.tab_panel.update_data(self.data)

def main():
    """
    Starts instance of application GUI and runs application
    """
    qt_app = QtWidgets.QApplication(sys.argv)
    gui = Gui()  # pylint: disable=W0612
    sys.exit(qt_app.exec())


if __name__ == '__main__':
    main()
