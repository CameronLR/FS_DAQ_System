import sys
import time
import numpy as np

from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QAction
import pyqtgraph

from DataProcessor import DataCollectorThread, Status, DAQ_Dataclass

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

        self.start_time_s = time.time()

        self.data_collection_thread = DataCollectorThread(self)
        self.status_signal.connect(
            self.data_collection_thread.status_signal_slot)
        self.data_collection_thread.data_signal.connect(
            self.received_data)
        self.data_collection_thread.start()

        self.init_tool_bar()

        self.setWindowTitle(f"FS DAQ Monitoring - {__VERSION__}")

        # x = np.linspace(-50, 50, 1000)
        # y = np.sin(x) / x

        self.speed_data = [[], []]

        x = 0
        y = 0

        self.graph_plots = []

        self.graph_widget = pyqtgraph.GraphicsLayoutWidget(show=True)

        last_graph = None

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

        self.setCentralWidget(self.graph_widget)

        self.showMaximized()

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

    @QtCore.Slot(DAQ_Dataclass)
    def received_data(self, data: DAQ_Dataclass):
        print("Received some data")
        print(f"SPEED = {data.speed_fl}")
        print(f"SPEED = {data.speed_fr}")
        print(f"SPEED = {data.speed_rl}")
        print(f"SPEED = {data.speed_rr}")

        self.speed_data[0].append(int(data.speed_fl))
        self.speed_data[1].append(int(time.time() - self.start_time_s))

        self.graph_plots[0][1].setData(
            x=self.speed_data[1], y=self.speed_data[0])

    def init_gui(self):
        pass


def main():
    """
    Main window to loop GUI and run DRT class
    :return:
    """
    qt_app = QtWidgets.QApplication(sys.argv)
    gui = Gui()
    sys.exit(qt_app.exec())


if __name__ == '__main__':
    main()
