from PySide6 import QtWidgets, QtCore, QtGui
import pyqtgraph

from ..Settings_Interface import ParamDef, get_param_defs
from ..dialog.param_select import select_param

BAR_GRAPH_LBL_FONT = QtGui.QFont("Arial", 14, QtGui.QFont.Bold)
LIVE_VALUE_LBL_FONT = QtGui.QFont("Arial", 18, QtGui.QFont.Bold)

class BarGraph(QtWidgets.QWidget):
    def __init__(self, param_idx):
        super(BarGraph, self).__init__()

        self.param_idx = param_idx
        
        param_defs = get_param_defs()
        param_def: ParamDef = param_defs[param_idx]

        v_layout = QtWidgets.QVBoxLayout()

        ## Create Bar Graph # TODO Align bar graph in centre
        container1 = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        plot = pyqtgraph.plot()
        self.bar_graph = pyqtgraph.BarGraphItem(x = 0, height = 10, width = 0.01)
        plot.hideAxis('bottom')
        plot.addItem(self.bar_graph)
        plot.setBackground("w")
        plot.setMaximumWidth(100)
        plot.setLabels(right=' ')
        layout.addWidget(plot, alignment=QtCore.Qt.AlignCenter)
        container1.setLayout(layout)

        ## Create live data label
        container = QtWidgets.QWidget()
        value_layout = QtWidgets.QVBoxLayout()
        value_layout.setAlignment(QtCore.Qt.AlignBottom)
        self.current_value = QtWidgets.QLabel("0.0")
        self.current_value.setAlignment(QtCore.Qt.AlignCenter)
        self.current_value.setFont(LIVE_VALUE_LBL_FONT)
        value_layout.addWidget(self.current_value)
        container.setLayout(value_layout)

        ## Stack current value over bar graph
        stacked_bar_graph = QtWidgets.QStackedLayout()
        stacked_bar_graph.setAlignment(QtCore.Qt.AlignBottom)
        stacked_bar_graph.addWidget(container1)
        stacked_bar_graph.addWidget(container)
        stacked_bar_graph.setStackingMode(QtWidgets.QStackedLayout.StackingMode.StackAll)

        ## Create Graph Label
        self.plot_label = QtWidgets.QLabel(param_def.name.replace(" ", "\n"))
        self.plot_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.plot_label.setFont(BAR_GRAPH_LBL_FONT)


        v_layout.addLayout(stacked_bar_graph)
        v_layout.addWidget(self.plot_label)

        self.setLayout(v_layout)
    
    def update_value(self, new_data):
        self.current_value.setText(str(new_data[self.param_idx]))
        self.bar_graph.setOpts(x = 0, height = new_data[self.param_idx], width = 0.01)

    def mousePressEvent(self, event):
        new_param_idx = select_param(self)

        if new_param_idx is not None:
            ## Change param
            param_defs = get_param_defs()
            print(f"@Change param to {param_defs[new_param_idx].name}")

            self.param_idx = new_param_idx
            self.plot_label.setText(param_defs[new_param_idx].name.replace(" ", "\n"))
            self.current_value.setText("0.0")

