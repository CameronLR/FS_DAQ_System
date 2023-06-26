import sys
sys.path.append("..") # Adds higher directory to python modules path.

import pyqtgraph

from ..Settings_Interface import ParamDef
from ..widget.line_graph_widget import GraphWidget


class GraphPanel(pyqtgraph.GraphicsLayoutWidget):
    def __init__(self, param_idx_list: list[int]):
        super(GraphPanel, self).__init__()

        self.setBackground("w")

        self.graph_list = []

        previous_graph = None

        for active_params, active_params_idx in enumerate(param_idx_list):

            graph_widget = GraphWidget(active_params_idx, 0)

            if previous_graph is not None:
                graph_widget.setXLink(previous_graph)
                previous_graph.getAxis('bottom').setTicks([])
            
            previous_graph = graph_widget
            self.addItem(graph_widget, active_params, 0)
            self.graph_list.append(graph_widget)

    def update_data(self, new_data):
        # TODO Add check that new data is not a bad size

        graph_widget: GraphWidget
        for graph_widget in self.graph_list:
            graph_widget.update_data(new_data)
