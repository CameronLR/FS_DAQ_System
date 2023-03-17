import sys
import time
import numpy as np

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QGridLayout
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
        self.speed_data = [[], []]

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

        self.live_objects = [[],[]]

        for i in range(0, DataGraphs.END):

            self.live_objects[0].append(QtWidgets.QVBoxLayout())

            object_label = QtWidgets.QLabel(GRAPH_Y_AXIS_LABEL[i])
            self.live_objects[1].append(QtWidgets.QLabel("0"))

            self.live_objects[0][i].addWidget(object_label)
            self.live_objects[0][i].addWidget(self.live_objects[1][i])

        hLayout_1 = QtWidgets.QHBoxLayout()
        hLayout_2 = QtWidgets.QHBoxLayout()
        hLayout_3 = QtWidgets.QHBoxLayout()

        hLayout_1.addLayout(self.live_objects[0][0])
        hLayout_1.addLayout(self.live_objects[0][1])
        hLayout_1.addLayout(self.live_objects[0][2])
    
        hLayout_2.addLayout(self.live_objects[0][3])
        hLayout_2.addLayout(self.live_objects[0][4])
        hLayout_2.addLayout(self.live_objects[0][5])
        
        hLayout_3.addLayout(self.live_objects[0][6])
        hLayout_3.addLayout(self.live_objects[0][7])
        hLayout_3.addLayout(self.live_objects[0][8])

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

    @QtCore.Slot(DAQ_Dataclass)
    def received_data(self, data: DAQ_Dataclass):
        print("Received some data")
        print(f"SPEED = {data.speed_fl}")
        print(f"SPEED = {data.speed_fr}")
        print(f"SPEED = {data.speed_rl}")
        print(f"SPEED = {data.speed_rr}")

        self.speed_data[0].append(int(data.speed_fl))
        self.speed_data[1].append(int(time.time() - self.start_time_s))

        if self.tab_widget.currentIndex() == 0:
            self.graph_plots[0][1].setData(
                x=self.speed_data[1], y=self.speed_data[0])
        else:
            self.live_objects[1][1].setText(str(self.speed_data[0][-1]))

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
