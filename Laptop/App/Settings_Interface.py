################################################################################
# Simple python file to interface with configuration file:
#   - Loads settings
#   - Saves settings
#
################################################################################

from dataclasses import dataclass
import configparser
import traceback

CONFIG_FILE_NAME = "./Config.ini"

@dataclass
class ParamDef:
    name: str
    unit: str
    variants: list[str]
    display_graph: bool
    display_live: bool
    low_value: float
    high_value: float

def is_true(string_value):
    return (string_value == "1")

def parse_variant_string(string_value):
    return None

def load():
    """Load settings located in config file
    return: dataclass instance of settings
    """
    config = configparser.ConfigParser()

    config.read(CONFIG_FILE_NAME)

    param_defs = []

    for param_idx in config['PARAM.OVERVIEW']:
        param_idx_str = f"PARAM.{config['PARAM.OVERVIEW'][param_idx]}"

        ## Figure out how best to parse variants

        try:
            param_defs.append(ParamDef(name=str(config[param_idx_str]['NAME']),
                                              unit=str(config[param_idx_str]['UNIT']),
                                              variants=parse_variant_string(config[param_idx_str]['VARIANTS']),
                                              display_graph=is_true(config[param_idx_str]['GRAPH']),
                                              display_live=is_true(config[param_idx_str]['LIVE']),
                                              low_value=float(config[param_idx_str]['LOW']),
                                              high_value=float(config[param_idx_str]['HIGH'])))
        except (ValueError, KeyError):
            print(f"Invalid paramater ({param_idx_str})\n{traceback.format_exc()}")

    return param_defs

######### Function not supported anymore #############
# def save(settings: Settings):
#     """Saves settings onto config file
#     param: settings: dataclass instance of settings
#     """
#     config = configparser.ConfigParser()

#     config['PARAM.OVERVIEW'] = {}

#     graph_data: ParamDef
#     for param_count, graph_data in enumerate(settings.active_parameters):
#         param_count += 1
#         config['PARAM.OVERVIEW'][f"param{param_count}"] = f"PARAM{param_count}"

#         config[f'PARAM.PARAM{param_count}'] = {"GRAPH_ACTIVE": 1 if graph_data.graph_active else 0,
#                                                "LIVE_ACTIVE": 1 if graph_data.live_active else 0,
#                                                "LABEL": graph_data.label,
#                                                "MIN_VALUE": graph_data.min_value,
#                                                "MAX_VALUE": graph_data.max_value,
#                                                "LIVE_WIDGET_TYPE": graph_data.live_widget_type}

#     config['SERIAL'] = {'Port': settings.serial_port,
#                         'Baud': settings.serial_baud}

#     with open(CONFIG_FILE_NAME, 'w') as config_file:
#         config.write(config_file)




# Experimental settings modification code - Note: code does not properly work

# class SettingsPopUp(QDialog):
#     def __init__(self, settings: Settings):
#         super().__init__()
#         self.setWindowTitle("Settings")
#         self.reload = False

#         self.settings = copy.deepcopy(settings)
#         self.graph_settings_line_list = []

#         self.dialog_layout = self.create_dialog_layout(settings.active_parameters)
#         self.setLayout(self.dialog_layout)

#     def create_dialog_layout(self, active_parameters):
#         dialog_layout = QtWidgets.QVBoxLayout()

#         grid_layout = QtWidgets.QGridLayout()

#         message = QtWidgets.QLabel("Set settings")
#         dialog_layout.addWidget(message)

#         self.graph_settings_line_list = []
#         for count, graph_data in enumerate(active_parameters):
#             graph_settings_line = ParameterSettingRow(self, count, graph_data)
#             self.graph_settings_line_list.append(graph_settings_line)

#             grid_layout.addWidget(graph_settings_line.graph_active, count, 0)
#             grid_layout.addWidget(graph_settings_line.live_active, count, 1)
#             grid_layout.addWidget(graph_settings_line.label, count, 2)
#             grid_layout.addWidget(graph_settings_line.min_value, count, 3)
#             grid_layout.addWidget(graph_settings_line.max_value, count, 4)
#             grid_layout.addWidget(graph_settings_line.live_widget_type, count, 5)
#             grid_layout.addWidget(graph_settings_line.delete_btn, count, 7)

#         dialog_layout.addLayout(grid_layout)

#         add_item_btn = QtWidgets.QPushButton("Add Item", self)
#         add_item_btn.clicked.connect(self.add_new_item)
#         dialog_layout.addWidget(add_item_btn)

#         self.dialog_btn_box = QtWidgets.QDialogButtonBox(
#             QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
#         self.dialog_btn_box.accepted.connect(self.accept)
#         self.dialog_btn_box.rejected.connect(self.reject)
#         dialog_layout.addWidget(self.dialog_btn_box)

#         return dialog_layout

#     def delete_item(self, idx):
#         self.settings.active_parameters.pop(idx)
#         print("INDEX ", idx, "\nDELETED ITEM - \n", self.settings.active_parameters)
#         self.reload = True
#         self.accept()

#     def add_new_item(self):
#         self.settings.active_parameters.append(ParamDef(False, False, "", 0, 0, LiveWidgetType.NUMERICAL, 1))
#         self.reload = True
#         self.accept()

#     def create_settings(self):
#         return Settings(active_parameters=[graph_settings.create_settings() for graph_settings in self.graph_settings_line_list],
#                         serial_port=self.settings.serial_port,
#                         serial_baud=self.settings.serial_baud)


# class ParameterSettingRow():
#     def __init__(self, parent, count, graph_settings: ParamDef):
#         self.setting_count = count
#         self.parent: SettingsPopUp = parent

#         self.nbr_label = QtWidgets.QLabel(str(count))
#         self.graph_active = QtWidgets.QCheckBox()
#         self.graph_active.setChecked(graph_settings.graph_active)
#         self.live_active = QtWidgets.QCheckBox()
#         self.live_active.setChecked(graph_settings.live_active)
#         self.label = QtWidgets.QTextEdit()
#         self.label.setMaximumHeight(20)
#         self.label.setText(graph_settings.label)
#         self.min_value = QtWidgets.QTextEdit()
#         self.min_value.setMaximumHeight(20)
#         self.min_value.setText(str(graph_settings.min_value))
#         self.max_value = QtWidgets.QTextEdit()
#         self.max_value.setMaximumHeight(20)
#         self.max_value.setText(str(graph_settings.max_value))
#         self.live_widget_type = QtWidgets.QComboBox()
#         self.live_widget_type.addItem(LiveWidgetType.NUMERICAL)
#         self.delete_btn = QtWidgets.QPushButton()
#         self.delete_btn.setIcon(QtGui.QIcon('delete_icon.png'))
#         self.delete_btn.clicked.connect(self.delete_self)

#     def delete_self(self):
#         print(f"Deleting Self, count={self.setting_count}, id={self}")
#         self.parent.delete_item(self.setting_count)

#     def create_settings(self):
#         return ParamDef(
#             graph_active=self.graph_active.checkState(),
#             live_active=self.live_active.checkState(),
#             label=self.label.toPlainText(),
#             min_value=self.min_value.toPlainText(),
#             max_value=self.max_value.toPlainText(),
#             live_widget_type=str(self.live_widget_type.currentText()),
#             unit_scale=1)


## Experimental setting pop-up

    # def on_settings(self):
    #     print("On Settings")

    #     new_settings = self.settings

    #     while (1):
    #         dlg = SettingsPopUp(new_settings)

    #         if dlg.exec_():
    #             new_settings = dlg.settings

    #             if not dlg.reload:
    #                 break
    #         else:
    #             new_settings = None
    #             break

    #     if new_settings is not None:
    #         self.para = new_settings




if __name__ == '__main__':
    print("NOTE: Module should not be run as main")
