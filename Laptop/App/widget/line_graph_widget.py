from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QLabel
import pyqtgraph

from ..param_def import ParamDef, get_param_def, get_param_defs
from ..dialog.param_select import select_param

## TODO Add support for multiple plots on one graph

class GraphWidget(pyqtgraph.PlotItem):
    def __init__(self, param_idx, graph_type=None):
        super(GraphWidget, self).__init__()

        self.param_idx = param_idx

        param_def = get_param_def(param_idx)

        self.setLabel("left", param_def.name)
        vb = self.getViewBox()
        vb.setBackgroundColor("w")
        
        pn = pyqtgraph.mkPen(color=(0, 0, 0), width=2)
        self.getAxis('left').setPen(pn)
        self.getAxis('bottom').setPen(pn)

        self.plot_data = self.plot([0],[0])

    def update_data(self, new_data):
        # Update Live Graph
        self.plot_data.setData(y=new_data[self.param_idx], x=new_data[-1])
    
    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.RightButton: # Only accept right clicks to allow pyqtgraph movement
            return

        new_param_idx = select_param(self)

        if new_param_idx is not None:
            ## Change param
            param_defs = get_param_defs()
            print(f"@Change param to {param_defs[new_param_idx].name}")

            self.setLabel("left", param_defs[new_param_idx].name)
            self.plot([0], [0])
