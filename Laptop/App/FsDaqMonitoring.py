################################################################################
# GUI Python File
#
#
#
################################################################################
import sys
from enum import Enum

from PySide6 import QtCore, QtWidgets, QtGui
import pyqtgraph

import serial.tools.list_ports

from DataCollector import DataCollectorThread, CollectorStatus, FsDaqData


__VERSION__ = "v1.0"


class GraphPlots(int, Enum):
    """Enum representing all the options for graph plots"""
    SPEED = 0
    THROTTLE = 1
    REVS = 2
    DAMPERS = 3
    FUEL = 4
    GEAR = 5
    WHEEL = 6
    STRAIN = 7
    GYRO = 8
    VOLTAGE = 9
    END = 10


GRAPH_Y_AXIS_LABEL = ["" for i in range(GraphPlots.END)]
GRAPH_Y_AXIS_LABEL[GraphPlots.SPEED] = "Speed (MPH)"
GRAPH_Y_AXIS_LABEL[GraphPlots.THROTTLE] = "Throttle (%)"
GRAPH_Y_AXIS_LABEL[GraphPlots.REVS] = "Revs (RPM)"
GRAPH_Y_AXIS_LABEL[GraphPlots.DAMPERS] = "Damper Position"
GRAPH_Y_AXIS_LABEL[GraphPlots.FUEL] = "Fuel Pressure"
GRAPH_Y_AXIS_LABEL[GraphPlots.GEAR] = "Gear Position"
GRAPH_Y_AXIS_LABEL[GraphPlots.WHEEL] = "Wheel Position"
GRAPH_Y_AXIS_LABEL[GraphPlots.STRAIN] = "Strain"
GRAPH_Y_AXIS_LABEL[GraphPlots.GYRO] = "Gyro"
GRAPH_Y_AXIS_LABEL[GraphPlots.VOLTAGE] = "Voltage (V)"


class Gui(QtWidgets.QMainWindow):
    status_signal = QtCore.Signal(int)

    def __init__(self):
        super(Gui, self).__init__()

        self.data = [[] for i in range(FsDaqData.END)]

        self.init_threads()

        self.setWindowTitle(f"FS DAQ Monitoring - {__VERSION__}")

        self.init_tool_bar()

        self.init_graph_widget()
        self.init_live_widget()

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

    def init_graph_widget(self):
        self.graph_plots = []

        self.graph_widget = pyqtgraph.GraphicsLayoutWidget(show=True)

        for i in range(0, GraphPlots.END):

            graph = pyqtgraph.PlotItem()
            plot = graph.plot([0], [0])

            self.graph_plots.append([graph, plot])

            graph.setLabel('left', GRAPH_Y_AXIS_LABEL[i])
            if i != 0:
                graph.setXLink(self.graph_plots[i-1][0])
            if i != GraphPlots.END - 1:
                graph.getAxis('bottom').setTicks([])

            self.graph_widget.addItem(graph, row=i, col=0)

        self.graph_widget.setBackground('w')

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


class LiveWidgetType(int, Enum):
    """Enum representing all the options for live monitoring widgets"""
    NUMERICAL = 0


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


def main():
    """
    Starts instance of application GUI and runs application
    """
    qt_app = QtWidgets.QApplication(sys.argv)
    gui = Gui()  # pylint: disable=W0612
    sys.exit(qt_app.exec())


if __name__ == '__main__':
    main()
