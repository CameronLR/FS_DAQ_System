import sys
sys.path.append("..") # Adds higher directory to python modules path.

import pyqtgraph

from ..Settings_Interface import ParamDef

class GraphPanel(pyqtgraph.GraphicsLayoutWidget):
    def __init__(self, param_settings: list[ParamDef]):
        super(GraphPanel, self).__init__()

        self.graph_plots = []

        graph_idx = 0

        previous_graph = None

        pn = pyqtgraph.mkPen(color=(0, 0, 0), width=2)

        for param_def in param_settings:
            if param_def.display_graph:
                graph, plot = self.create_graph_widget(param_def.name)

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
                graph_plot.setData(y=new_data[graph_idx], x=new_data[-1], color="blue")
                # TODO Look at how easy it would be to have multiple plot in one graph (different colours)



