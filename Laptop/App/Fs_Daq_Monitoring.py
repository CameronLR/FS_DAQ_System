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


class LiveWidgetType(str, Enum):
    """Enum representing all the options for live monitoring widgets"""
    NUMERICAL = "Numerical"


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
    active_guis: list[GuiParameters]
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

        self.live_widget = QtWidgets.QWidget()
        self.live_objects = []

        self.nbr_data_points = len(self.settings.active_guis)

        active_lives = 0
        active_graphs = 0

        active_gui: GuiParameters
        for count, active_gui in enumerate(self.settings.active_guis):
            if active_gui.graph_active:
                graph, plot = self.create_graph_widget(active_gui.label)
                if count != 0:
                    graph.setXLink(self.graph_plots[count-1][0])

                print(f"COUNT={count}, max = {self.nbr_data_points}")

                # date_axis = pyqtgraph.DateAxisItem(orientation='bottom')
                # graph.setAxisItems(axisItems={'bottom': date_axis})

                if count != self.nbr_data_points - 1:
                    graph.getAxis('bottom').setTicks([])
                else:
                    print(active_gui.label)

                self.graph_widget.addItem(graph, active_graphs, 0)

                active_graphs += 1

            else:
                graph, plot = None, None

            if active_gui.live_active:
                live_widget = self.create_live_widget(active_gui.label)
                active_lives += 1
            else:
                live_widget = None

            self.graph_plots.append([graph, plot])
            self.live_objects.append(live_widget)

        self.graph_widget.setBackground('w')

        if active_lives < 10:
            dimensions = 3
        else:
            dimensions = 4

        v_layout = QtWidgets.QVBoxLayout()
        offset = 0
        for x in range(dimensions):
            h_layout = QtWidgets.QHBoxLayout()
            for y in range(dimensions):
                # print(f"x={x}, y={y}, offset={offset}, idx={x*dimensions+y+offset}")
                if x*dimensions+y+offset >= len(self.live_objects):
                    continue

                while (self.live_objects[x*dimensions+y+offset] is None):
                    offset += 1

                h_layout.addWidget(self.live_objects[x*dimensions+y+offset].widget)

            v_layout.addLayout(h_layout)

        self.live_widget.setLayout(v_layout)

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

    def create_graph_widget(self, label):
        graph = pyqtgraph.PlotItem(axisItems={'bottom': pyqtgraph.DateAxisItem()})
        plot = graph.plot([0], [0])

        graph.setLabel("left", label)

        return graph, plot

        # graph.setXLink(graph)

    def create_live_widget(self, label):
        return LiveWidget(LiveWidgetType.NUMERICAL, label)

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

        self.serial_port_selector = QtWidgets.QComboBox()
        self.serial_port_selector.view().pressed.connect(self.populate_serial_combo)

        self.populate_serial_combo()

        tool_bar.addWidget(self.serial_port_selector)

    def populate_serial_combo(self):
        self.serial_port_selector.clear()
        for port, description, _ in sorted(serial.tools.list_ports.comports()):
            self.serial_port_selector.addItem(f"{port} - {description}")

    def on_settings(self):
        print("Entering Settings")

        dlg = SettingsPopUp(self.settings)
        if dlg.exec():
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
        for i in range(self.nbr_data_points + 2):
            self.data[i].append(input_data[i])

        if self.tab_widget.currentIndex() == 0:
            self.update_graphs()
        else:
            self.update_live()

    def update_graphs(self):
        """Updates graph plots in live tab
        """
        for count, active_gui in enumerate(self.settings.active_guis):
            if active_gui.graph_active:
                self.graph_plots[count][1].setData(y=self.data[count], x=self.data[FsDaqData.TIME])

    def update_live(self):
        """Updates widgets in live tab
        """
        for count, active_gui in enumerate(self.settings.active_guis):
            if active_gui.live_active:
                self.live_objects[count].update_value(self.data[count][-1])

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


EMPTY_SETTINGS_ITEM = GuiParameters(False, False, "", 0, 0, LiveWidgetType.NUMERICAL)


class SettingsPopUp(QDialog):
    def __init__(self, settings: Settings):
        super().__init__()

        self.settings = settings

        self.setWindowTitle("Settings")

        apply_btn = QtWidgets.QDialogButtonBox.Ok
        close_btn = QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.setLayout(self.create_v_layout(settings.active_guis))

    def create_v_layout(self, active_guis):
        self.graph_settings_line_list = []
        v_layout = QtWidgets.QVBoxLayout()

        grid_layout = QtWidgets.QGridLayout()

        message = QtWidgets.QLabel("Set settings")
        v_layout.addWidget(message)

        for count, graph_data in enumerate(active_guis):
            graph_settings_line = GraphSettingsLine(self, count, graph_data)
            self.graph_settings_line_list.append(graph_settings_line)

            grid_layout.addWidget(graph_settings_line.graph_active, count, 0)
            grid_layout.addWidget(graph_settings_line.live_active, count, 1)
            grid_layout.addWidget(graph_settings_line.label, count, 2)
            grid_layout.addWidget(graph_settings_line.min_value, count, 3)
            grid_layout.addWidget(graph_settings_line.max_value, count, 4)
            grid_layout.addWidget(graph_settings_line.live_widget_type, count, 5)
            grid_layout.addWidget(graph_settings_line.delete_btn, count, 7)

        v_layout.addLayout(grid_layout)

        self.delete_btn = QtWidgets.QPushButton("Add Item", self)
        self.delete_btn.clicked.connect(self.add_new_item)

        v_layout.addWidget(self.delete_btn)

        return v_layout

    def delete_item(self, idx):
        self.settings.active_guis.pop(idx)
        self.setLayout(self.create_v_layout(self.settings.active_guis))
        print("INDEX ", idx, "\nDELETED ITEM - \n", self.settings.active_guis)

    def add_new_item(self):
        self.settings.active_guis.append(GuiParameters(False, False, "", 0, 0, LiveWidgetType.NUMERICAL))
        self.setLayout(self.create_v_layout(self.settings.active_guis))


class GraphSettingsLine(QtWidgets.QHBoxLayout):
    def __init__(self, parent, count, graph_settings: GuiParameters):
        super().__init__()
        self.setting_count = count
        self.parent: SettingsPopUp = parent
        self.nbr_label = QtWidgets.QLabel(str(count))
        self.graph_active = QtWidgets.QCheckBox()
        self.graph_active.setChecked(graph_settings.graph_active)
        self.live_active = QtWidgets.QCheckBox()
        self.live_active.setChecked(graph_settings.live_active)
        self.label = QtWidgets.QTextEdit()
        self.label.setMaximumHeight(20)
        self.label.setText(graph_settings.label)
        self.min_value = QtWidgets.QTextEdit()
        self.min_value.setMaximumHeight(20)
        self.min_value.setText(str(graph_settings.min_value))
        self.max_value = QtWidgets.QTextEdit()
        self.max_value.setMaximumHeight(20)
        self.max_value.setText(str(graph_settings.max_value))
        self.live_widget_type = QtWidgets.QComboBox()
        self.live_widget_type.addItem(LiveWidgetType.NUMERICAL)
        self.delete_btn = QtWidgets.QPushButton()
        self.delete_btn.setIcon(QtGui.QIcon('delete_icon.png'))
        self.delete_btn.clicked.connect(self.delete_self)

    def delete_self(self):
        self.parent.delete_item(self.setting_count)

    def update_settings(self, graph_settings: GuiParameters):
        graph_settings.graph_active = self.graph_active.checkState()
        graph_settings.live_active = self.live_active.checkState()
        graph_settings.label = self.label.toPlainText()
        graph_settings.min_value = self.min_value.toPlainText()
        graph_settings.max_value = self.max_value.toPlainText()


def main():
    """
    Starts instance of application GUI and runs application
    """
    qt_app = QtWidgets.QApplication(sys.argv)
    gui = Gui()  # pylint: disable=W0612
    sys.exit(qt_app.exec())


if __name__ == '__main__':
    main()
