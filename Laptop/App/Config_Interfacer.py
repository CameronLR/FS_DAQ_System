################################################################################
# Simple python file to interface with configuration file:
#   - Loads settings
#   - Saves settings
#
################################################################################

import configparser
from Fs_Daq_Monitoring import Settings, GuiParameters

CONFIG_FILE_NAME = "./Laptop/App/Config.ini"


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

        active_guis.append(GuiParameters(graph_active=graph_active,
                                         live_active=live_active,
                                         label=config['GRAPH.'+idx]['LABEL'],
                                         min_value=config['GRAPH.'+idx]['MIN_VALUE'],
                                         max_value=config['GRAPH.'+idx]['MAX_VALUE'],
                                         live_widget_type=config['GRAPH.'+idx]['LIVE_WIDGET_TYPE']))

    serial_port = config.get('SERIAL', 'PORT')
    serial_baud = config.get('SERIAL', 'BAUD')

    return Settings(active_guis, serial_port, serial_baud)


def save(settings: Settings):
    """Saves settings onto config file
    param: settings: dataclass instance of settings
    """

    config = configparser.ConfigParser()

    config['GRAPH.OVERVIEW'] = {}

    graph_data: GuiParameters
    for param_count, graph_data in enumerate(settings.active_guis):
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

    with open(CONFIG_FILE_NAME+"2", 'w') as configFile:
        config.write(configFile)
