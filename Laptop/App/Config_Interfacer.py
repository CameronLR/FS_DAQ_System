################################################################################
# Simple python file to interface with configuration file:
#   - Loads settings
#   - Saves settings
#
################################################################################

import configparser
from Fs_Daq_Monitoring import Settings, GraphParameters, LiveParameters

CONFIG_FILE_NAME = "Config.ini"


def load():
    """Load settings located in config file
    return: dataclass instance of settings
    """
    config = configparser.ConfigParser()

    config.read(CONFIG_FILE_NAME)

    serial_port = config['SERIAL']['Port']
    serial_baud = config['SERIAL']['Baud']

    return Settings(None, None, serial_port, serial_baud)


def save(settings: Settings):
    """Saves settings onto config file
    param: settings: dataclass instance of settings
    """

    config = configparser.ConfigParser()

    for graph_data in settings.active_graphs:
        if len(graph_data) != 6:
            print(f"ERROR: Invalid number of paramters in configuration - \n{graph_data}")
            continue

        config['GRAPH'] = {graph_data.name: graph_data}

    config['SERIAL'] = {'Port': settings.serial_port,
                        'Baud': settings.serial_baud}

    with open(CONFIG_FILE_NAME, 'w') as configFile:
        config.write(configFile)
