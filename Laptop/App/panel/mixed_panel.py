from PySide6 import QtWidgets

from ..widget.line_graph_widget import GraphWidget
from ..widget.live_widget import LiveWidget, LiveWidgetType
from ..widget.bar_graph_widget import BarGraph


class MixedPanel(QtWidgets.QWidget):
    def __init__(self, settings):
        super(MixedPanel, self).__init__()

        left_layout = QtWidgets.QVBoxLayout()

        graph_panel = LineGraphPanel(settings)
        live_panel = LiveInfoPanel(settings)

        left_layout.addWidget(graph_panel)
        left_layout.addWidget(live_panel)

        main_layout = QtWidgets.QHBoxLayout()

        bar_graph_widget = BarGraphPanel(settings)

        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(bar_graph_widget, 2)

        self.setLayout(main_layout)


    def update_data(new_data):
        # Update Live Graph
        pass

        # Update Live Value

class BarGraphPanel(QtWidgets.QWidget):
    def __init__(self, settings):
        super(BarGraphPanel, self).__init__()

        self.bar_graphs = []
        
        h_layout = QtWidgets.QHBoxLayout()
        
        bar1 = BarGraph("TEST1")
        bar3 = BarGraph("TEST2")
        bar2 = BarGraph("TEST3")

        h_layout.addWidget(bar1)
        h_layout.addWidget(bar2)
        h_layout.addWidget(bar3)

        self.setLayout(h_layout)



class LiveInfoPanel(QtWidgets.QWidget):
    def __init__(self, settings):
        super(LiveInfoPanel, self).__init__()

        self.live_widgets = []

        h_layout = QtWidgets.QHBoxLayout()

        widget1 = LiveWidget(LiveWidgetType.NUMERICAL, "TEST 1")
        widget2 = LiveWidget(LiveWidgetType.NUMERICAL, "TEST 2")
        widget3 = LiveWidget(LiveWidgetType.NUMERICAL, "TEST 3")



        h_layout.addWidget(widget1)
        h_layout.addWidget(widget2)
        h_layout.addWidget(widget3)

        self.setLayout(h_layout)


class LineGraphPanel(QtWidgets.QWidget):
    def __init__(self, settings):
        super(LineGraphPanel, self).__init__()

        v_layout = QtWidgets.QVBoxLayout()

        graph1 = GraphWidget("Test1")
        graph2 = GraphWidget("Test2")

        v_layout.addWidget(graph1)
        v_layout.addWidget(graph2)

        self.setLayout(v_layout)

