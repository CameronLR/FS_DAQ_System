from PySide6 import QtWidgets

from ..widget.line_graph_widget import GraphWidget
from ..widget.live_widget import LiveWidget, LiveWidgetType
from ..widget.bar_graph_widget import BarGraph
from ..panel.graph_panel import GraphPanel


class MixedPanel(QtWidgets.QWidget):
    def __init__(self, settings):
        super(MixedPanel, self).__init__()

        left_layout = QtWidgets.QVBoxLayout()

        self.graph_panel = GraphPanel([0,1,2])
        self.live_panel = LiveInfoPanel(settings)

        left_layout.addWidget(self.graph_panel)
        left_layout.addWidget(self.live_panel)

        main_layout = QtWidgets.QHBoxLayout()

        self.bar_graph_widget = BarGraphPanel(settings)

        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(self.bar_graph_widget, 2)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 0)

        self.setLayout(main_layout)

    def update_data(self, new_data):
        self.graph_panel.update_data(new_data)
        self.live_panel.update_data(new_data)
        self.bar_graph_widget.update_data(new_data)
        
class BarGraphPanel(QtWidgets.QWidget):
    def __init__(self, settings):
        super(BarGraphPanel, self).__init__()

        self.bar_graphs = []
        
        h_layout = QtWidgets.QHBoxLayout()
        
        bar1 = BarGraph(0)
        bar3 = BarGraph(1)
        bar2 = BarGraph(2)

        h_layout.addWidget(bar1)
        h_layout.addWidget(bar2)
        h_layout.addWidget(bar3)
        

        h_layout.setSpacing(0)
        h_layout.addStretch(1)

        self.setLayout(h_layout)



class LiveInfoPanel(QtWidgets.QWidget):
    def __init__(self, settings):
        super(LiveInfoPanel, self).__init__()

        self.live_widgets = []

        h_layout = QtWidgets.QHBoxLayout()

        widget1 = LiveWidget(0)
        widget2 = LiveWidget(1)
        widget3 = LiveWidget(2)



        h_layout.addWidget(widget1)
        h_layout.addWidget(widget2)
        h_layout.addWidget(widget3)

        self.setLayout(h_layout)

