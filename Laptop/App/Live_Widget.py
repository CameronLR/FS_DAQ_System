#################### Live Monitoring Widget Management ####################

from enum import Enum
from PySide6 import QtCore, QtWidgets, QtGui


class LiveWidgetType(str, Enum):
    """Enum representing all the options for live monitoring widgets"""
    NUMERICAL = "Numerical"


LIVE_WIDGET_LBL_FONT = QtGui.QFont("Arial", 28, QtGui.QFont.Bold)
LIVE_WIDGET_VALUE_FONT = QtGui.QFont("Arial", 40, QtGui.QFont.Bold)


class LiveWidget():
    def __init__(self, widget_type, label):
        self.widget_type = widget_type
        self.value = None
        self.widget = self.get_live_monitor_widget(widget_type, label)

    def get_live_monitor_widget(self, widget_type, label):
        if widget_type == LiveWidgetType.NUMERICAL:
            return self.get_numerical_widget(label)

        print("ERROR: Invalid widget type")

    def get_numerical_widget(self, label):
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel(label)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFont(LIVE_WIDGET_LBL_FONT)
        self.value = QtWidgets.QLabel("0")
        self.value.setAlignment(QtCore.Qt.AlignCenter)
        self.value.setFont(LIVE_WIDGET_VALUE_FONT)

        layout.addWidget(label)
        layout.addWidget(self.value)

        frame.setLayout(layout)

        return frame

    def update_value(self, value):
        if self.widget_type == LiveWidgetType.NUMERICAL:
            self.value.setText(str(value))
        else:
            print("ERROR: Invalid widget type")

if __name__ == '__main__':
    print("NOTE: Module should not be run as main")
