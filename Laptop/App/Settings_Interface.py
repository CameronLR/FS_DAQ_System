################################################################################
# Simple python file to interface with configuration file:
#   - Loads settings
#   - Saves settings
#
################################################################################

from dataclasses import dataclass
import copy
import configparser

from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QDialog

from Live_Widget import LiveWidgetType

CONFIG_FILE_NAME = "./Config.ini"


@dataclass
class ParameterSettings:
    graph_active: bool
    live_active: bool
    label: str
    min_value: int
    max_value: int
    live_widget_type: LiveWidgetType
    unit_scale: int


@dataclass
class Settings:
    active_parameters: list[ParameterSettings]
    serial_port: str
    serial_baud: int


def load():
    """Load settings located in config file
    return: dataclass instance of settings
    """
    config = configparser.ConfigParser()

    config.read(CONFIG_FILE_NAME)

    active_guis = []

    for thing in config['GRAPH.OVERVIEW']:
        idx = config['GRAPH.OVERVIEW'][thing]

        if config['GRAPH.'+idx]['GRAPH_ACTIVE'] == "1":
            graph_active = True
        else:
            graph_active = False

        if config['GRAPH.'+idx]['LIVE_ACTIVE'] == "1":
            live_active = True
        else:
            live_active = False

        active_guis.append(ParameterSettings(graph_active=graph_active,
                                             live_active=live_active,
                                             label=config['GRAPH.'+idx]['LABEL'],
                                             min_value=config['GRAPH.'+idx]['MIN_VALUE'],
                                             max_value=config['GRAPH.'+idx]['MAX_VALUE'],
                                             live_widget_type=config['GRAPH.'+idx]['LIVE_WIDGET_TYPE'],
                                             unit_scale=1))

    serial_port = config.get('SERIAL', 'PORT')
    serial_baud = config.get('SERIAL', 'BAUD')

    return Settings(active_guis, serial_port, serial_baud)


def save(settings: Settings):
    """Saves settings onto config file
    param: settings: dataclass instance of settings
    """
    config = configparser.ConfigParser()

    config['GRAPH.OVERVIEW'] = {}

    graph_data: ParameterSettings
    for param_count, graph_data in enumerate(settings.active_parameters):
        param_count += 1
        config['GRAPH.OVERVIEW'][f"param{param_count}"] = f"PARAM{param_count}"

        config[f'GRAPH.PARAM{param_count}'] = {"GRAPH_ACTIVE": 1 if graph_data.graph_active else 0,
                                               "LIVE_ACTIVE": 1 if graph_data.live_active else 0,
                                               "LABEL": graph_data.label,
                                               "MIN_VALUE": graph_data.min_value,
                                               "MAX_VALUE": graph_data.max_value,
                                               "LIVE_WIDGET_TYPE": graph_data.live_widget_type}

    config['SERIAL'] = {'Port': settings.serial_port,
                        'Baud': settings.serial_baud}

    with open(CONFIG_FILE_NAME, 'w') as config_file:
        config.write(config_file)

# Experimental settings modification code - Note: code does not properly work

class SettingsPopUp(QDialog):
    def __init__(self, settings: Settings):
        super().__init__()
        self.setWindowTitle("Settings")

        self.settings = copy.deepcopy(settings)
        self.graph_settings_line_list = []

        self.dialog_layout = self.create_dialog_layout(settings.active_guis)
        self.setLayout(self.dialog_layout)

    def create_dialog_layout(self, active_guis):
        dialog_layout = QtWidgets.QVBoxLayout()

        grid_layout = QtWidgets.QGridLayout()

        message = QtWidgets.QLabel("Set settings")
        dialog_layout.addWidget(message)

        self.graph_settings_line_list = []
        for count, graph_data in enumerate(active_guis):
            graph_settings_line = ParameterSettingRow(self, count, graph_data)
            self.graph_settings_line_list.append(graph_settings_line)

            grid_layout.addWidget(graph_settings_line.graph_active, count, 0)
            grid_layout.addWidget(graph_settings_line.live_active, count, 1)
            grid_layout.addWidget(graph_settings_line.label, count, 2)
            grid_layout.addWidget(graph_settings_line.min_value, count, 3)
            grid_layout.addWidget(graph_settings_line.max_value, count, 4)
            grid_layout.addWidget(graph_settings_line.live_widget_type, count, 5)
            grid_layout.addWidget(graph_settings_line.delete_btn, count, 7)

        dialog_layout.addLayout(grid_layout)

        add_item_btn = QtWidgets.QPushButton("Add Item", self)
        add_item_btn.clicked.connect(self.add_new_item)
        dialog_layout.addWidget(add_item_btn)

        self.dialog_btn_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.dialog_btn_box.accepted.connect(self.accept)
        self.dialog_btn_box.rejected.connect(self.reject)
        dialog_layout.addWidget(self.dialog_btn_box)

        return dialog_layout

    def delete_item(self, idx):
        self.settings.active_guis.pop(idx)
        self.dialog_layout = None
        self.dialog_layout = self.create_dialog_layout(self.settings.active_guis)
        self.setLayout(self.dialog_layout)
        print("INDEX ", idx, "\nDELETED ITEM - \n", self.settings.active_guis)

    def add_new_item(self):
        self.settings.active_guis.append(ParameterSettings(False, False, "", 0, 0, LiveWidgetType.NUMERICAL, 1))
        self.dialog_layout = None
        self.dialog_layout = self.create_dialog_layout(self.settings.active_guis)
        self.setLayout(self.dialog_layout)

    def create_settings(self):
        return Settings(active_parameters=[graph_settings.create_settings() for graph_settings in self.graph_settings_line_list],
                        serial_port=self.settings.serial_port,
                        serial_baud=self.settings.serial_baud)


class ParameterSettingRow():
    def __init__(self, parent, count, graph_settings: ParameterSettings):
        self.setting_count = count
        self.parent: SettingsPopUp = parent

        self.nbr_label = QtWidgets.QLabel(str(count))
        self.graph_active = QtWidgets.QCheckBox()
        self.graph_active.setChecked(graph_settings.graph_active)
        self.live_active = QtWidgets.QCheckBox()
        self.live_active.setChecked(graph_settings.live_active)
        self.label = QtWidgets.QTextEdit()
        self.label.setMaximumHeight(20)
        self.label.setText(graph_settings.label)
        self.min_value = QtWidgets.QTextEdit()
        self.min_value.setMaximumHeight(20)
        self.min_value.setText(str(graph_settings.min_value))
        self.max_value = QtWidgets.QTextEdit()
        self.max_value.setMaximumHeight(20)
        self.max_value.setText(str(graph_settings.max_value))
        self.live_widget_type = QtWidgets.QComboBox()
        self.live_widget_type.addItem(LiveWidgetType.NUMERICAL)
        self.delete_btn = QtWidgets.QPushButton()
        self.delete_btn.setIcon(QtGui.QIcon('delete_icon.png'))
        self.delete_btn.clicked.connect(self.delete_self)

    def delete_self(self):
        print(f"Deleting Self, count={self.setting_count}, id={self}")
        self.parent.delete_item(self.setting_count)

    def create_settings(self):
        return ParameterSettings(
            graph_active=self.graph_active.checkState(),
            live_active=self.live_active.checkState(),
            label=self.label.toPlainText(),
            min_value=self.min_value.toPlainText(),
            max_value=self.max_value.toPlainText(),
            live_widget_type=str(self.live_widget_type.currentText()),
            unit_scale=1)


if __name__ == '__main__':
    print("NOTE: Module should not be run as main")
