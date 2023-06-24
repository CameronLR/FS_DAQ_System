import sys
sys.path.append("..") # Adds higher directory to python modules path.

from PySide6 import QtWidgets

from ..widget.live_widget import LiveWidget, LiveWidgetType
from ..Settings_Interface import ParamDef

class LivePanel(QtWidgets.QWidget):
    def __init__(self, param_settings: list[ParamDef]):
        super(LivePanel, self).__init__()

        self.live_objects = []

        live_idx = 0

        for param_setting in param_settings:
            if param_setting.display_live:
                live_widget = LiveWidget(LiveWidgetType.NUMERICAL, param_setting.name)
                live_idx += 1
            else:
                live_widget = None

            self.live_objects.append(live_widget)

        self.load_live_widgets(live_idx)

    def load_live_widgets(self, nbr_live_widgets):
        # Currently only parameters up to 16 is properly supported
        if nbr_live_widgets > 12:
            nbr_hrz_widgets = 4
            nbr_vrt_widgets = 4
        elif nbr_live_widgets > 9:
            nbr_hrz_widgets = 4
            nbr_vrt_widgets = 3
        else:
            nbr_hrz_widgets = 3
            nbr_vrt_widgets = 3

        v_layout = QtWidgets.QVBoxLayout()

       # remaining_spaces = (dimensions**2) - active_lives

        widget_idx_offset = 0

        widget_idx = 0

        for v_idx in range(nbr_vrt_widgets):
            h_layout = QtWidgets.QHBoxLayout()

            for h_idx in range(nbr_hrz_widgets):
                # print(f"x={x}, y={y}, offset={offset}, idx={x*x_dimensions+y+offset}")

                if widget_idx >= len(self.live_objects):
                    widget_idx += 1
                    print(f"IDX to big, {len(self.live_objects)}")
                    continue

                while (self.live_objects[widget_idx] is None):
                    widget_idx += 1
                    print("Skipping")

                print(self.live_objects[widget_idx].label)
                print(widget_idx)

                h_layout.addWidget(self.live_objects[widget_idx])
                widget_idx += 1

            v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

    def update_data(self, new_data):
        """Updates widgets in live tab
        """
        live_plot: LiveWidget
        for live_idx, live_plot in enumerate(self.live_objects):
            if live_plot.live_active:
                self.live_objects[live_idx].update_value(new_data[live_idx][-1])

