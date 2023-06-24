from PySide6 import QtWidgets, QtCore, QtGui
import pyqtgraph

LIVE_WIDGET_VALUE_FONT = QtGui.QFont("Arial", 40, QtGui.QFont.Bold)
LIVE_WIDGET_LBL_FONT = QtGui.QFont("Arial", 28, QtGui.QFont.Bold)

class BarGraph(QtWidgets.QWidget):
    def __init__(self, label):
        super(BarGraph, self).__init__()

        v_layout = QtWidgets.QVBoxLayout()

        ## Create Bar Graph # TODO Align bar graph in centre
        plot = pyqtgraph.plot()
        self.bar_graph = pyqtgraph.BarGraphItem(x = [0], height = [10], width = 0.01)
        plot.hideAxis('bottom')
        plot.addItem(self.bar_graph)
        plot.setBackground("w")
        plot.setMaximumWidth(100)

        ## Create live data label
        self.current_value = QtWidgets.QLabel("0.0")
        self.current_value.setAlignment(QtCore.Qt.AlignCenter)
        self.current_value.setFont(LIVE_WIDGET_VALUE_FONT)

        ## Stack current value over bar graph
        stacked_bar_graph = QtWidgets.QStackedLayout()
        stacked_bar_graph.addWidget(plot)
        stacked_bar_graph.addWidget(self.current_value)
        stacked_bar_graph.setStackingMode(QtWidgets.QStackedLayout.StackingMode.StackAll)

        ## Create Graph Label
        plot_label = QtWidgets.QLabel(label)
        plot_label.setAlignment(QtCore.Qt.AlignCenter)
        plot_label.setFont(LIVE_WIDGET_LBL_FONT)


        v_layout.addLayout(stacked_bar_graph)
        v_layout.addWidget(plot_label)

        self.setLayout(v_layout)
    
    def update_value(self, value):
        self.current_value.setText(str(value))
        self.bar_graph.setOpts(x = [0], height = [value], width = 0.01)
    


