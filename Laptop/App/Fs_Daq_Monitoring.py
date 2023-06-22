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
    settings_signal = QtCore.Signal(str)

    def __init__(self):
        super(Gui, self).__init__()
        self.setWindowTitle(f"FS DAQ Monitoring - {__VERSION__}")

        self.settings: Settings = Settings_Interface.load()
        self.serial_port = None

        self.init_threads()
        self.init_tool_bar()

        self.graph_widget = GraphPanel(self.settings.active_parameters)
        self.live_widget = LivePanel(self.settings.active_parameters)

        self.nbr_data_points = len(self.settings.active_parameters) + 1  # Plus one to include time
        self.data = [[] for _ in range(self.nbr_data_points)]

        self.tab_widget = QtWidgets.QTabWidget()

        self.tab_widget.addTab(self.graph_widget, "Graph View")
        self.tab_widget.addTab(self.live_widget, "Live View")

        self.setCentralWidget(self.tab_widget)

        self.showMaximized()

    def init_threads(self):
        data_collection_thread = DataCollectorThread(self, self.settings)
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

        if self.tab_widget.currentIndex() == 0:
            self.graph_widget.update_data(self.data)
        else:
            self.update_live()

    def update_graphs(self):
        """Updates graph plots in live tab
        """
        for graph_idx, graph_plot in enumerate(self.graph_widget.graph_plots):
            if graph_plot is not None:
                graph_plot.setData(y=self.data[graph_idx], x=self.data[-1], color="blue")
                # TODO Look at how easy it would be to have multiple plot in one graph (different colours)

    def update_live(self):
        """Updates widgets in live tab
        """
        for count, active_gui in enumerate(self.settings.active_parameters):
            if active_gui.live_active:
                self.live_objects[count].update_value(self.data[count][-1])


class LivePanel(QtWidgets.QWidget):
    def __init__(self, param_settings: list[ParameterSettings]):
        super(LivePanel, self).__init__()

        self.live_objects = []

        live_idx = 0

        for param_idx, param_setting in enumerate(param_settings):
            if param_setting.live_active:
                live_widget = LiveWidget(LiveWidgetType.NUMERICAL, param_setting.label)
                live_idx += 1
                print(param_setting.label)
            else:
                live_widget = None

            self.live_objects.append(live_widget)

        self.load_live_widgets(live_idx)

    def load_live_widgets(self, nbr_live_widgets):
        # Currently only parameters up to 16 is properly supported
        if nbr_live_widgets > 12:
            nbr_hrz_widgets = 4
            nbr_vrt_widgets = 4
        elif nbr_live_widgets > 9:
            nbr_hrz_widgets = 4
            nbr_vrt_widgets = 3
        else:
            nbr_hrz_widgets = 3
            nbr_vrt_widgets = 3

        v_layout = QtWidgets.QVBoxLayout()

       # remaining_spaces = (dimensions**2) - active_lives

        widget_idx_offset = 0

        widget_idx = 0

        for v_idx in range(nbr_vrt_widgets):
            h_layout = QtWidgets.QHBoxLayout()

            for h_idx in range(nbr_hrz_widgets):
                # print(f"x={x}, y={y}, offset={offset}, idx={x*x_dimensions+y+offset}")

                if widget_idx >= len(self.live_objects):
                    widget_idx += 1
                    print("IDX to big, " + len(self.live_objects))
                    continue

                while (self.live_objects[widget_idx] is None):
                    widget_idx += 1
                    print("Skipping")

                print(self.live_objects[widget_idx].label)
                print(widget_idx)

                h_layout.addWidget(self.live_objects[widget_idx].widget)
                widget_idx += 1

            v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

    def update_live(self, new_data):
        """Updates widgets in live tab
        """
        live_plot: LiveWidget
        for live_idx, live_plot in enumerate(self.live_objects):
            if live_plot.live_active:
                self.live_objects[live_idx].update_value(new_data[live_idx][-1])


class GraphPanel(pyqtgraph.GraphicsLayoutWidget):
    def __init__(self, param_settings: list[ParameterSettings]):
        super(GraphPanel, self).__init__()

        self.graph_plots = []

        graph_idx = 0

        previous_graph = None

        pn = pyqtgraph.mkPen(color=(0, 0, 0), width=2)

        for param_idx, param_setting in enumerate(param_settings):
            if param_setting.graph_active:
                graph, plot = self.create_graph_widget(param_setting.label)

                if previous_graph is not None:
                    graph.setXLink(previous_graph)
                    previous_graph.getAxis('bottom').setTicks([])

                # date_axis = pyqtgraph.DateAxisItem(orientation='bottom')
                # graph.setAxisItems(axisItems={'bottom': date_axis})

                self.addItem(graph, graph_idx, 0)

                graph_idx += 1

                graph.getAxis('left').setPen(pn)
                graph.getAxis('bottom').setPen(pn)

                previous_graph = graph

            else:
                graph, plot = None, None

            self.graph_plots.append([graph, plot])

        self.setBackground('w')

    def create_graph_widget(self, label):
        graph = pyqtgraph.PlotItem(axisItems={'bottom': pyqtgraph.DateAxisItem()})
        plot = graph.plot([0], [0])

        graph.setLabel("left", label)

        return graph, plot

    def update_data(self, new_data):
        # TODO Add check that new data is not a bad size

        for graph_idx, graph_plot in enumerate(self.graph_plots):
            if graph_plot is not None:
                graph_plot.setData(y=new_data[graph_idx], x=new_data[-1])


def main():
    """
    Starts instance of application GUI and runs application
    """
    qt_app = QtWidgets.QApplication(sys.argv)
    gui = Gui()  # pylint: disable=W0612
    sys.exit(qt_app.exec())


if __name__ == '__main__':
    main()
