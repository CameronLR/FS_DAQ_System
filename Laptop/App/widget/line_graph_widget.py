from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QLabel
import pyqtgraph

## TODO Add support for multiple plots on one graph

LIVE_WIDGET_VALUE_FONT = QtGui.QFont("Arial", 40, QtGui.QFont.Bold)

class GraphWidget(QtWidgets.QWidget):
    def __init__(self, label: str):
        super(GraphWidget, self).__init__()

        v_layout = QtWidgets.QHBoxLayout()

        # Create Label Widget
        label_widget = HrzLabel(label)

        # Create Graph Widget
        graph_widget = pyqtgraph.PlotWidget()
        self.plot_data = graph_widget.plot([0],[0])
        graph_widget.setBackground("w")

        # Create Live Data Widget
        self.current_value = QtWidgets.QLabel("0")
        self.current_value.setAlignment(QtCore.Qt.AlignCenter)
        self.current_value.setFont(LIVE_WIDGET_VALUE_FONT)

        v_layout.addWidget(label_widget)
        v_layout.addWidget(graph_widget)
        v_layout.addWidget(self.current_value)

        self.setLayout(v_layout)


    def update_data(self, new_data, time_data):
        # Update Live Graph
        self.plot_data.setData(y=new_data, x=time_data)

        # Update Live Value
        self.current_value.setText(str(new_data[-1]))



class HrzLabel(QLabel):
    def __init__(self, *args):
        QLabel.__init__(self, *args)

    # def paintEvent(self, event):
    #     pass
    #     painter = QtGui.QPainter(self)
    #     painter.setPen(QtCore.Qt.black)
    #     painter.translate(20, 100)
    #     painter.rotate(-90)
    #     painter.drawText(0, 0, "hellos")
    #     painter.end()

    #     pass
    #     print("Paint Event")
    #     QLabel.paintEvent(self, event)
    #     painter = QtGui.QPainter (self)
    #     painter.translate(0, self.height()-1)
    #     painter.rotate(-90)
    #     self.setGeometry(self.x(), self.y(), self.height(), self.width())
    #     painter.end
    #     QLabel.render(self, painter)