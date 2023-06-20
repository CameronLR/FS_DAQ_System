################################################################################
# GUI Python File
#
#
#
################################################################################
import sys

from PySide6 import QtCore, QtWidgets, QtGui
import pyqtgraph

import serial.tools.list_ports

from Live_Widget import LiveWidget, LiveWidgetType
from Data_Collector import DataCollectorThread, CollectorStatus
import Settings_Interface
from Settings_Interface import Settings, ParameterSettings, SettingsPopUp


__VERSION__ = "v1.0"


class Gui(QtWidgets.QMainWindow):
    status_signal = QtCore.Signal(int)

    def __init__(self):
        super(Gui, self).__init__()

        self.settings: Settings = Settings_Interface.load()

        self.init_threads()

        self.setWindowTitle(f"FS DAQ Monitoring - {__VERSION__}")

        self.init_tool_bar()

        self.graph_plots = []
        self.graph_widget = pyqtgraph.GraphicsLayoutWidget(show=True)

        self.live_objects = []
        self.live_widget = QtWidgets.QWidget()

        self.nbr_data_points = len(self.settings.active_parameters)
        self.data = [[] for _ in range(self.nbr_data_points)]

        active_lives = 0
        active_graphs = 0

        active_gui: ParameterSettings
        for count, active_gui in enumerate(self.settings.active_parameters):
            if active_gui.graph_active:
                graph, plot = self.create_graph_widget(active_gui.label)
                if count != 0:
                    graph.setXLink(self.graph_plots[count-1][0])

                # date_axis = pyqtgraph.DateAxisItem(orientation='bottom')
                # graph.setAxisItems(axisItems={'bottom': date_axis})

                if count != self.nbr_data_points - 1:
                    graph.getAxis('bottom').setTicks([])

                self.graph_widget.addItem(graph, active_graphs, 0)

                active_graphs += 1

            else:
                graph, plot = None, None

            if active_gui.live_active:
                live_widget = LiveWidget(LiveWidgetType.NUMERICAL, active_gui.label)
                active_lives += 1
                print(active_gui.label)
            else:
                live_widget = None

            self.graph_plots.append([graph, plot])
            self.live_objects.append(live_widget)

        self.graph_widget.setBackground('w')

        # Currently only parameters up to 16 is properly supported
        if active_lives > 12:
            x_dimensions = 4
            y_dimensions = 4
        elif active_lives > 9:
            x_dimensions = 4
            y_dimensions = 3
        else:
            x_dimensions = 3
            y_dimensions = 3

        print(f"x={x_dimensions},y={y_dimensions}")

        v_layout = QtWidgets.QVBoxLayout()

       # remaining_spaces = (dimensions**2) - active_lives

        offset = 0
        for x in range(x_dimensions):
            h_layout = QtWidgets.QHBoxLayout()

            for y in range(y_dimensions):
                print(f"x={x}, y={y}, offset={offset}, idx={x*x_dimensions+y+offset}")
                if x*x_dimensions+y+offset >= len(self.live_objects):
                    continue

                while (self.live_objects[x*x_dimensions+y+offset] is None):
                    offset += 1

                h_layout.addWidget(self.live_objects[x*x_dimensions+y+offset].widget)

            v_layout.addLayout(h_layout)

        self.live_widget.setLayout(v_layout)

        self.tab_widget = QtWidgets.QTabWidget()

        self.tab_widget.addTab(self.graph_widget, "Graph View")
        self.tab_widget.addTab(self.live_widget, "Live View")

        self.setCentralWidget(self.tab_widget)

        self.showMaximized()

    def init_threads(self):
        self.data_collection_thread = DataCollectorThread(self, self.settings)
        self.status_signal.connect(self.data_collection_thread.status_signal_slot)
        self.data_collection_thread.data_signal.connect(self.received_data)
        self.data_collection_thread.start()

    def create_graph_widget(self, label):
        graph = pyqtgraph.PlotItem(axisItems={'bottom': pyqtgraph.DateAxisItem()})
        plot = graph.plot([0], [0])

        graph.setLabel("left", label)

        return graph, plot

    def init_tool_bar(self):
        tool_bar = QtWidgets.QToolBar()
        self.addToolBar(tool_bar)

        # settings_btn = QtGui.QAction("Settings", self)
        # settings_btn.triggered.connect(self.on_settings)
        # tool_bar.addAction(settings_btn)

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
        for i in range(self.nbr_data_points + 1):  # Plus one to account for time input
            self.data[i].append(input_data[i])

        if self.tab_widget.currentIndex() == 0:
            self.update_graphs()
        else:
            self.update_live()

    def update_graphs(self):
        """Updates graph plots in live tab
        """
        for count, active_gui in enumerate(self.settings.active_parameters):
            if active_gui.graph_active:
                self.graph_plots[count][1].setData(y=self.data[count], x=self.data[-1])

    def update_live(self):
        """Updates widgets in live tab
        """
        for count, active_gui in enumerate(self.settings.active_parameters):
            if active_gui.live_active:
                self.live_objects[count].update_value(self.data[count][-1])


def main():
    """
    Starts instance of application GUI and runs application
    """
    qt_app = QtWidgets.QApplication(sys.argv)
    gui = Gui()  # pylint: disable=W0612
    sys.exit(qt_app.exec())


if __name__ == '__main__':
    main()
