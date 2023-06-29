from PySide6 import QtWidgets

from .mixed_panel import MixedPanel
from .graph_panel import GraphPanel
from .live_panel import LivePanel

from ..Settings_Interface import ParamDef


class MainTabPanel(QtWidgets.QTabWidget):
    def __init__(self, param_defs):
        super(MainTabPanel, self).__init__()

        
        self.mixed_widget = MixedPanel(param_defs)
        self.live_widget = LivePanel(param_defs)

        active_graph_params = []
        param_def: ParamDef
        for param_idx, param_def in enumerate(param_defs):
            if param_def.display_graph:
                active_graph_params.append(param_idx)
        
        self.graph_widget = GraphPanel(active_graph_params)

        self.addTab(self.mixed_widget, "Mixed View")
        self.addTab(self.graph_widget, "Graph View")
        self.addTab(self.live_widget, "Live View")

    def update_data(self, new_data):
        if self.currentIndex() == 0:
            self.mixed_widget.update_data(new_data)
        elif self.currentIndex() == 1:
            self.graph_widget.update_data(new_data)
        else:
            self.live_widget.update_data(new_data)


