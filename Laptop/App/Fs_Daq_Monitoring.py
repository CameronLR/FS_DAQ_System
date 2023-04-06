################################################################################
# GUI Python File
#
#
#
################################################################################
import sys
from enum import Enum
from dataclasses import dataclass

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QDialog
# from PySide6.QtWidgets.QDialog import QDialogButtonBox

import pyqtgraph

import serial.tools.list_ports

from Data_Collector import DataCollectorThread, CollectorStatus, FsDaqData
import Config_Interfacer


__VERSION__ = "v1.0"


class LiveWidgetType(int, Enum):
    """Enum representing all the options for live monitoring widgets"""
    NUMERICAL = 0


@dataclass
class GuiParameters:
    graph_active: bool
    live_active: bool
    label: str
    min_value: int
    max_value: int
    live_widget_type: LiveWidgetType


@dataclass
class Settings:
    active_guis: list(GuiParameters)
    serial_port: str
    serial_baud: int


class Gui(QtWidgets.QMainWindow):
    status_signal = QtCore.Signal(int)

    def __init__(self):
        super(Gui, self).__init__()

        self.settings = Config_Interfacer.load()

        self.data = [[] for i in range(FsDaqData.END)]

        self.init_threads()

        self.setWindowTitle(f"FS DAQ Monitoring - {__VERSION__}")

        self.init_tool_bar()

        self.graph_plots = []
        self.graph_widget = pyqtgraph.GraphicsLayoutWidget(show=True)

        for active_gui, count in enumerate(self.settings.active_guis):
            self.graph_plots.append(self.init_graph_widget(active_gui.label))
            self.init_live_widget()
            self.graph_widget.addItem(self.graph_plots[count][0], count, 0)

        self.graph_widget.setBackground('w')

        self.tab_widget = QtWidgets.QTabWidget()

        self.tab_widget.addTab(self.graph_widget, "Graph View")
        self.tab_widget.addTab(self.live_widget, "Live View")

        self.setCentralWidget(self.tab_widget)

        self.showMaximized()

    def init_threads(self):
        self.data_collection_thread = DataCollectorThread(self)
        self.status_signal.connect(self.data_collection_thread.status_signal_slot)
        self.data_collection_thread.data_signal.connect(self.received_data)
        self.data_collection_thread.start()

    def init_graph_widget(self, label):
        graph = pyqtgraph.PlotItem()
        plot = graph.plot([0], [0])

        self.graph_plots.append([graph, plot])

        graph.setXLink(graph)

    def init_live_widget(self):

        self.live_widget = QtWidgets.QWidget()

        self.live_objects: list(LiveWidget) = []

        for i in range(0, GraphPlots.END):
            self.live_objects.append(LiveWidget(
                LiveWidgetType.NUMERICAL, GRAPH_Y_AXIS_LABEL[i]))

        h_layout_1 = QtWidgets.QHBoxLayout()
        h_layout_2 = QtWidgets.QHBoxLayout()
        h_layout_3 = QtWidgets.QHBoxLayout()

        h_layout_1.addWidget(self.live_objects[0].widget)
        h_layout_1.addWidget(self.live_objects[1].widget)
        h_layout_1.addWidget(self.live_objects[2].widget)

        h_layout_2.addWidget(self.live_objects[3].widget)
        h_layout_2.addWidget(self.live_objects[4].widget)
        h_layout_2.addWidget(self.live_objects[5].widget)

        h_layout_3.addWidget(self.live_objects[6].widget)
        h_layout_3.addWidget(self.live_objects[7].widget)
        h_layout_3.addWidget(self.live_objects[8].widget)

        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        v_layout.addLayout(h_layout_3)

        self.live_widget.setLayout(v_layout)

    def init_tool_bar(self):
        tool_bar = QtWidgets.QToolBar()
        self.addToolBar(tool_bar)

        settings_btn = QtGui.QAction("Settings", self)
        settings_btn.triggered.connect(self.on_settings)
        tool_bar.addAction(settings_btn)

        stop_btn = QtGui.QAction("Stop", self)
        stop_btn.triggered.connect(self.on_stop_monitoring)
        tool_bar.addAction(stop_btn)

        start_btn = QtGui.QAction("Start", self)
        start_btn.triggered.connect(self.on_start_monitoring)
        tool_bar.addAction(start_btn)

        serial_port_label = QtWidgets.QLabel()
        serial_port_label.setText("Serial Port: ")
        tool_bar.addWidget(serial_port_label)

        serial_port_selector = QtWidgets.QComboBox()

        for port, description, _ in sorted(serial.tools.list_ports.comports()):
            serial_port_selector.addItem(f"{port} - {description}")

        tool_bar.addWidget(serial_port_selector)

    def on_settings(self):
        print("Entering Settings")

        dlg = SettingsPopUp(self.settings)
        if dlg.exec_():
            Config_Interfacer.save(dlg.settings)
            self.settings = dlg.settings
        else:
            print("Cancel!")

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
        for i in range(FsDaqData.END):
            self.data[i].append(input_data[i])

        if self.tab_widget.currentIndex() == 0:
            self.update_graphs()
        else:
            self.update_live()

    def update_graphs(self):
        """Updates graph plots in live tab
        """
        self.graph_plots[GraphPlots.SPEED][1].setData(
            y=self.data[FsDaqData.WHL_SPEED_FR], x=self.data[FsDaqData.TIME])
        self.graph_plots[GraphPlots.REVS][1].setData(
            y=self.data[FsDaqData.ENGINE_REVS], x=self.data[FsDaqData.TIME])
        self.graph_plots[GraphPlots.DAMPERS][1].setData(
            y=self.data[FsDaqData.DAMPER_POS_FR], x=self.data[FsDaqData.TIME])
        self.graph_plots[GraphPlots.GEAR][1].setData(
            y=self.data[FsDaqData.GEAR_POS], x=self.data[FsDaqData.TIME])
        self.graph_plots[GraphPlots.WHEEL][1].setData(
            y=self.data[FsDaqData.STR_WHL_POS], x=self.data[FsDaqData.TIME])
        self.graph_plots[GraphPlots.GYRO][1].setData(
            y=self.data[FsDaqData.GYRO_X], x=self.data[FsDaqData.TIME])
        self.graph_plots[GraphPlots.VOLTAGE][1].setData(
            y=self.data[FsDaqData.BAT_VOLT], x=self.data[FsDaqData.TIME])
        self.graph_plots[GraphPlots.THROTTLE][1].setData(
            y=self.data[FsDaqData.THROTTLE], x=self.data[FsDaqData.TIME])
        self.graph_plots[GraphPlots.FUEL][1].setData(
            y=self.data[FsDaqData.FUEL_PRESSURE], x=self.data[FsDaqData.TIME])

    def update_live(self):
        """Updates widgets in live tab
        """
        self.live_objects[GraphPlots.SPEED].update_value(
            self.data[FsDaqData.WHL_SPEED_FR][-1])
        self.live_objects[GraphPlots.REVS].update_value(
            self.data[FsDaqData.ENGINE_REVS][-1])
        self.live_objects[GraphPlots.DAMPERS].update_value(
            self.data[FsDaqData.DAMPER_POS_FR][-1])
        self.live_objects[GraphPlots.GEAR].update_value(
            self.data[FsDaqData.GEAR_POS][-1])
        self.live_objects[GraphPlots.WHEEL].update_value(
            self.data[FsDaqData.STR_WHL_POS][-1])
        self.live_objects[GraphPlots.GYRO].update_value(
            self.data[FsDaqData.GYRO_X][-1])
        self.live_objects[GraphPlots.VOLTAGE].update_value(
            self.data[FsDaqData.BAT_VOLT][-1])
        self.live_objects[GraphPlots.THROTTLE].update_value(
            self.data[FsDaqData.THROTTLE][-1])
        self.live_objects[GraphPlots.FUEL].update_value(
            self.data[FsDaqData.FUEL_PRESSURE][-1])

    def init_gui(self):
        pass

#################### Live Monitoring Widget Management ####################


LIVE_WIDGET_LBL_FONT = QtGui.QFont("Arial", 28, QtGui.QFont.Bold)
LIVE_WIDGET_VALUE_FONT = QtGui.QFont("Arial", 40, QtGui.QFont.Bold)


class LiveWidget():
    def __init__(self, widget_type, label):
        self.widget_type = widget_type
        self.value = None
        self.widget = self.get_live_monitor_widget(widget_type, label)

    def get_live_monitor_widget(self, widget_type, label):
        if widget_type == LiveWidgetType.NUMERICAL:
            return self.get_numerical_widget(label)

        print("ERROR: Invalid widget type")

    def get_numerical_widget(self, label):
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel(label)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(LIVE_WIDGET_LBL_FONT)
        self.value = QtWidgets.QLabel("0")
        self.value.setAlignment(QtCore.Qt.AlignCenter)
        self.value.setFont(LIVE_WIDGET_VALUE_FONT)

        layout.addWidget(label)
        layout.addWidget(self.value)

        frame.setLayout(layout)

        return frame

    def update_value(self, value):
        if self.widget_type == LiveWidgetType.NUMERICAL:
            self.value.setText(str(value))
        else:
            print("ERROR: Invalid widget type")


class SettingsPopUp(QDialog):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.setWindowTitle("Settings")

        apply_btn = QtWidgets.QDialogButtonBox.Ok
        close_btn = QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Set settings")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


def main():
    """
    Starts instance of application GUI and runs application
    """
    qt_app = QtWidgets.QApplication(sys.argv)
    gui = Gui()  # pylint: disable=W0612
    sys.exit(qt_app.exec())


if __name__ == '__main__':
    main()
