#################### Live Monitoring Widget Management ####################

from enum import Enum
from PySide6 import QtCore, QtWidgets, QtGui

from ..dialog.param_select import select_param
from ..param_def import ParamDef, get_param_def, get_param_defs


class LiveWidgetType(str, Enum):
    """Enum representing all the options for live monitoring widgets"""
    NUMERICAL = "Numerical"


LIVE_WIDGET_LBL_FONT = QtGui.QFont("Arial", 28, QtGui.QFont.Bold)
LIVE_WIDGET_VALUE_FONT = QtGui.QFont("Arial", 40, QtGui.QFont.Bold)


class LiveWidget(QtWidgets.QFrame):
    def __init__(self, param_idx):
        super(LiveWidget, self).__init__()
        self.param_idx = param_idx
        self.param_def = get_param_def(param_idx)

        self.setFrameStyle(QtWidgets.QFrame.WinPanel | QtWidgets.QFrame.Raised)
        self.setLineWidth(4)

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel(self.param_def.name)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFont(LIVE_WIDGET_LBL_FONT)

        self.value = QtWidgets.QLabel("0")
        self.value.setAlignment(QtCore.Qt.AlignCenter)
        self.value.setFont(LIVE_WIDGET_VALUE_FONT)

        layout.addWidget(self.label)
        layout.addWidget(self.value)

        self.setLayout(layout)

    def update_value(self, new_data):
        param_data = new_data[self.param_idx]
        param_current_value = param_data[-1]
        self.value.setText(str(param_current_value))
            
    def mousePressEvent(self, event):
        print("TRYING TO OPEN DIALOG")
        new_param_idx = select_param(self)
        print("HEY")

        if new_param_idx is not None:
            ## Change param
            param_defs = get_param_defs()
            print(f"@Change param to {param_defs[new_param_idx].name}")

            self.label.setText(param_defs[new_param_idx].name)
            self.value.setText("0.0")
            









if __name__ == '__main__':
    print("NOTE: Module should not be run as main")
