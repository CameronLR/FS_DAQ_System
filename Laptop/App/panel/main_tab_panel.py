from PySide6 import QtWidgets

from .mixed_panel import MixedPanel
from .graph_panel import GraphPanel
from .live_panel import LivePanel


class MainTabPanel(QtWidgets.QTabWidget):
    def __init__(self, settings):
        super(MainTabPanel, self).__init__()

        
        self.mixed_widget = MixedPanel(settings)
        self.graph_widget = GraphPanel(settings)
        self.live_widget = LivePanel(settings)

        self.addTab(self.mixed_widget, "Mixed View")
        self.addTab(self.graph_widget, "Graph View")
        self.addTab(self.live_widget, "Live View")

    def update_data(self, new_data):
        if self.tab_widget.currentIndex() == 0:
            self.mixed_widget.update_data(new_data)
        elif self.tab_widget.currentIndex() == 1:
            self.graph_widget.update_data(new_data)
        else:
            self.live_widget.update_data(new_data)


