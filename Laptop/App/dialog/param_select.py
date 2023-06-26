from PySide6 import QtGui, QtWidgets

from ..Settings_Interface import get_param_defs, ParamDef

class ParamSelectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, param_defs=None):
        super().__init__()
        self.setWindowTitle("Select Parameter:")

        nbr_of_params = len(param_defs)

        # TODO Expand param defs to include Avg and variants (currently on average is done)

        v_layout = QtWidgets.QVBoxLayout()

        self.list_widget = QtWidgets.QListWidget()
        for param_idx in range(nbr_of_params):
            QtWidgets.QListWidgetItem(param_defs[param_idx], self.list_widget)

        select_btn = QtWidgets.QPushButton('Select')
        select_btn.clicked.connect(self.accept)

        v_layout.addWidget(self.list_widget)
        v_layout.addWidget(select_btn)

        self.setLayout(v_layout)


def select_param(parent):
    # Create list of param names
    param_list = []
    params: ParamDef
    for params in get_param_defs():
        param_list.append(params.name)

    param_select = ParamSelectDialog(parent, param_list)

    if param_select.exec():
        # Change param
        print(f"Changing Param to {param_select.list_widget.currentItem().text()}")
        return param_select.list_widget.currentRow()

    print("Do nothing!")
    return None
