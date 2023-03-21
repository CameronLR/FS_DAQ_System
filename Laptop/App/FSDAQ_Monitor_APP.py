import sys
import time

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QAction
import pyqtgraph

import DataProcessor
from DataProcessor import DataCollectorThread, Status, DAQ_DataPoints

from enum import Enum

__VERSION__ = "v1.0"


class DataGraphs(int, Enum):
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


GRAPH_Y_AXIS_LABEL = ["" for i in range(DataGraphs.END)]
GRAPH_Y_AXIS_LABEL[DataGraphs.SPEED] = "Speed (MPH)"
GRAPH_Y_AXIS_LABEL[DataGraphs.THROTTLE] = "Throttle (%)"
GRAPH_Y_AXIS_LABEL[DataGraphs.REVS] = "Revs (RPM)"
GRAPH_Y_AXIS_LABEL[DataGraphs.DAMPERS] = "Damper Position"
GRAPH_Y_AXIS_LABEL[DataGraphs.FUEL] = "Fuel Pressure"
GRAPH_Y_AXIS_LABEL[DataGraphs.GEAR] = "Gear Position"
GRAPH_Y_AXIS_LABEL[DataGraphs.WHEEL] = "Wheel Position"
GRAPH_Y_AXIS_LABEL[DataGraphs.STRAIN] = "Strain"
GRAPH_Y_AXIS_LABEL[DataGraphs.GYRO] = "Gyro"
GRAPH_Y_AXIS_LABEL[DataGraphs.VOLTAGE] = "Voltage (V)"


class Gui(QtWidgets.QMainWindow):
    status_signal = QtCore.Signal(int)

    def __init__(self):
        super(Gui, self).__init__()

        self.data = [[] for i in range(DAQ_DataPoints.END)]

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
        self.status_signal.connect(
            self.data_collection_thread.status_signal_slot)
        self.data_collection_thread.data_signal.connect(
            self.received_data)
        self.data_collection_thread.start()

    def init_graph_widget(self):
        self.graph_plots = []

        self.graph_widget = pyqtgraph.GraphicsLayoutWidget(show=True)

        for i in range(0, DataGraphs.END):

            graph = pyqtgraph.PlotItem()
            plot = graph.plot([0], [0])

            self.graph_plots.append([graph, plot])

            graph.setLabel('left', GRAPH_Y_AXIS_LABEL[i])
            if i != 0:
                graph.setXLink(self.graph_plots[i-1][0])
            if i != DataGraphs.END - 1:
                graph.getAxis('bottom').setTicks([])

            self.graph_widget.addItem(graph, row=i, col=0)

        self.graph_widget.setBackground('w')

    def init_live_widget(self):

        self.live_widget = QtWidgets.QWidget()

        self.live_objects: list(LiveMonitorWidget) = []

        for i in range(0, DataGraphs.END):
            self.live_objects.append(LiveMonitorWidget(
                LiveMonitorWidgetType.NUMERICAL, GRAPH_Y_AXIS_LABEL[i]))

        hLayout_1 = QtWidgets.QHBoxLayout()
        hLayout_2 = QtWidgets.QHBoxLayout()
        hLayout_3 = QtWidgets.QHBoxLayout()

        hLayout_1.addWidget(self.live_objects[0].widget)
        hLayout_1.addWidget(self.live_objects[1].widget)
        hLayout_1.addWidget(self.live_objects[2].widget)

        hLayout_2.addWidget(self.live_objects[3].widget)
        hLayout_2.addWidget(self.live_objects[4].widget)
        hLayout_2.addWidget(self.live_objects[5].widget)

        hLayout_3.addWidget(self.live_objects[6].widget)
        hLayout_3.addWidget(self.live_objects[7].widget)
        hLayout_3.addWidget(self.live_objects[8].widget)

        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addLayout(hLayout_1)
        vLayout.addLayout(hLayout_2)
        vLayout.addLayout(hLayout_3)

        self.live_widget.setLayout(vLayout)

    def init_tool_bar(self):
        tool_bar = QtWidgets.QToolBar()
        self.addToolBar(tool_bar)

        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.on_stop_monitoring)
        tool_bar.addAction(stop_btn)

        start_btn = QAction("Start", self)
        start_btn.triggered.connect(self.on_start_monitoring)
        tool_bar.addAction(start_btn)

    def on_start_monitoring(self):
        print("Starting monitoring")
        self.status_signal.emit(Status.RUNNING)

    def on_stop_monitoring(self):
        print("Stopping monitoring")
        self.status_signal.emit(Status.STOPPED)

    @QtCore.Slot(object)
    def received_data(self, input_data):
        print("Received some data")

        for i in range(DAQ_DataPoints.END):
            self.data[i].append(input_data[i])

        print(
            f"SPEED = {self.data[DAQ_DataPoints.WHL_SPEED_FL]} \nTIME = {self.data[DAQ_DataPoints.TIME]}")

        if self.tab_widget.currentIndex() == 0:
            self.update_graphs()
        else:
            self.update_live()

    def update_graphs(self):
        self.graph_plots[DataGraphs.SPEED][1].setData(
            y=self.data[DAQ_DataPoints.WHL_SPEED_FR], x=self.data[DAQ_DataPoints.TIME])
        self.graph_plots[DataGraphs.REVS][1].setData(
            y=self.data[DAQ_DataPoints.ENGINE_REVS], x=self.data[DAQ_DataPoints.TIME])
        self.graph_plots[DataGraphs.DAMPERS][1].setData(
            y=self.data[DAQ_DataPoints.DAMPER_POS_FR], x=self.data[DAQ_DataPoints.TIME])
        self.graph_plots[DataGraphs.GEAR][1].setData(
            y=self.data[DAQ_DataPoints.GEAR_POS], x=self.data[DAQ_DataPoints.TIME])
        self.graph_plots[DataGraphs.WHEEL][1].setData(
            y=self.data[DAQ_DataPoints.STR_WHL_POS], x=self.data[DAQ_DataPoints.TIME])
        self.graph_plots[DataGraphs.GYRO][1].setData(
            y=self.data[DAQ_DataPoints.GYRO_X], x=self.data[DAQ_DataPoints.TIME])
        self.graph_plots[DataGraphs.VOLTAGE][1].setData(
            y=self.data[DAQ_DataPoints.BAT_VOLT], x=self.data[DAQ_DataPoints.TIME])
        self.graph_plots[DataGraphs.THROTTLE][1].setData(
            y=self.data[DAQ_DataPoints.THROTTLE], x=self.data[DAQ_DataPoints.TIME])
        self.graph_plots[DataGraphs.FUEL][1].setData(
            y=self.data[DAQ_DataPoints.FUEL_PRESSURE], x=self.data[DAQ_DataPoints.TIME])

    def update_live(self):
        self.live_objects[DataGraphs.SPEED].update_value(
            self.data[DAQ_DataPoints.WHL_SPEED_FR][-1])
        self.live_objects[DataGraphs.REVS].update_value(
            self.data[DAQ_DataPoints.ENGINE_REVS][-1])
        self.live_objects[DataGraphs.DAMPERS].update_value(
            self.data[DAQ_DataPoints.DAMPER_POS_FR][-1])
        self.live_objects[DataGraphs.GEAR].update_value(
            self.data[DAQ_DataPoints.GEAR_POS][-1])
        self.live_objects[DataGraphs.WHEEL].update_value(
            self.data[DAQ_DataPoints.STR_WHL_POS][-1])
        self.live_objects[DataGraphs.GYRO].update_value(
            self.data[DAQ_DataPoints.GYRO_X][-1])
        self.live_objects[DataGraphs.VOLTAGE].update_value(
            self.data[DAQ_DataPoints.BAT_VOLT][-1])
        self.live_objects[DataGraphs.THROTTLE].update_value(
            self.data[DAQ_DataPoints.THROTTLE][-1])
        self.live_objects[DataGraphs.FUEL].update_value(
            self.data[DAQ_DataPoints.FUEL_PRESSURE][-1])

    def init_gui(self):
        pass


class LiveMonitorWidgetType(int, Enum):
    NUMERICAL = 0


LIVE_WIDGET_LBL_FONT = QtGui.QFont("Arial", 28, QtGui.QFont.Bold)
LIVE_WIDGET_VALUE_FONT = QtGui.QFont("Arial", 40, QtGui.QFont.Bold)


def main():
    """
    Main window to loop GUI and run DRT class
    :return:
    """
    qt_app = QtWidgets.QApplication(sys.argv)
    gui = Gui()
    sys.exit(qt_app.exec())


class LiveMonitorWidget():
    def __init__(self, widget_type, label):
        self.widget_type = widget_type
        self.value = None
        self.widget = self.get_live_monitor_widget(widget_type, label)

    def get_live_monitor_widget(self, widget_type, label):
        if widget_type == LiveMonitorWidgetType.NUMERICAL:
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
        if self.widget_type == LiveMonitorWidgetType.NUMERICAL:
            self.value.setText(str(value))
        else:
            print("ERROR: Invalid widget type")


if __name__ == '__main__':
    main()
