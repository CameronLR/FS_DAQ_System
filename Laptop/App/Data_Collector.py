################################################################################
# DataCollector Python File
#
#
#
################################################################################
import time
import random
from enum import Enum

from .Settings_Interface import ParamDef

import serial

from PySide6 import QtCore

class CollectorStatus(int, Enum):
    """Enum representing the data collector's state"""
    RUNNING = 1
    STOPPED = 2


class DataCollectorThread(QtCore.QThread):
    data_signal = QtCore.Signal(object)

    def __init__(self, parent, param_defs, dummy_data_enabled: bool):
        super(DataCollectorThread, self).__init__(parent=parent)
        self.dummy_data_enabled = dummy_data_enabled
        self.status = CollectorStatus.STOPPED

        self.start_time = int(time.time())
        self.last_time = int(time.time())

        self.param_defs: list[ParamDef]
        self.param_defs = param_defs

        self.start_time = 0

        try:
            self.serial = serial.Serial("COM5", "115200", timeout=1)
        except serial.SerialException:
            print("ERROR: Could not open serial port")
            self.serial = None
        else:
            self.serial.close()

    def run(self):
        """Main runner function of DataCollector,
             - Processes and posts data to GUI in RUNNING mode
             - Sits in IDLE in STOPPED mode
        """
        while 1:
            if self.status == CollectorStatus.STOPPED:
                # TODO find out if we need to keep flushing here to keep serial buffer clear
                time.sleep(0.5)
            else:
                self.listen()
                time.sleep(0.1)

    @QtCore.Slot(str)
    def settings_signal_slot(self, serial_port):
        """Qt Slot to set serial port of DataCollector
        :param settings: Settings: settings to set
        """
        print(serial_port)

        # self.set_serial_settings(settings.serial_port, settings.serial_baud)

        # self.active_parameters = settings.active_guis

    def set_serial_settings(self, serial_port, serial_baud):
        """Set Serial Settings
        :param serial_port: str: serial port name to open
        :param serial_baud: int: serial baud rate to set
        """
        if self.serial.is_open:
            self.serial.close()

        try:
            self.serial = serial.Serial(serial_port, serial_baud, timeout=1)
        except serial.SerialException:
            print("ERROR: Could not open serial port")
            self.serial = None
        else:
            if self.status == CollectorStatus.STOPPED:
                self.serial.close()
            elif self.status == CollectorStatus.RUNNING:
                self.serial.open()
                self.serial.flush()

    @QtCore.Slot(int)
    def status_signal_slot(self, status_sig):
        """Qt Slot to receive commands to start/stop DataCollector
        :param status_sig: CollectorStatus enum representing status
        """
        self.status = status_sig
        if self.status == CollectorStatus.STOPPED:
            print("Stopping Data Collector")
            # Close Serial Port
            if self.serial is not None:
                self.serial.close()
        elif self.status == CollectorStatus.RUNNING:
            print("Starting Data Collector")
            # Open Serial Port
            if self.serial is not None:
                print("Opening serial!")
                self.serial.open()
                self.serial.flush()

        else:
            print("ERROR: Invalid status")
            self.status = CollectorStatus.STOPPED

    def generate_dummy_data(self):
        dummy_data = []

        for param_def in self.param_defs:
            dummy_data.append(float(random.randint(0,100)))

        dummy_data.append(float(self.last_time - self.start_time))

        return dummy_data

    def listen(self):
        """ Keeps processing and posting serial data until serial port is free
        """
        serial_data = " "

        if self.dummy_data_enabled and (self.last_time != int(time.time())):
            self.last_time = int(time.time())
            self.data_signal.emit(self.generate_dummy_data())
        else:
            # TODO Figure out why _overlapper_read isn't working for Ethan
            while self.serial is not None and self.serial.is_open and self.serial._overlapped_read is not None:
                serial_data = self.serial.readline()

                if serial_data is None:
                    break

                processed_data = self.process_serial_data(serial_data)

                if processed_data is not None:
                    self.data_signal.emit(processed_data)

    def process_serial_data(self, serial_data):
        """Process serial data
          - Run CRC checks on input data
          - Extract necessary data into list
          - TODO Add future possible processing here? 
        :param serial_data: serial data to process
        :return: list of processed data, None if error occurs
        """
        decoded_data = serial_data.decode("utf-8")

        if not self.is_crc_valid(decoded_data):
            return None

        return self.extract_data(decoded_data)

    def is_crc_valid(self, serial_data):
        """Checks whether CRC is valid in serial data
        # TODO Implement function
        """
        _ = serial_data
        return True

    def extract_data(self, serial_data):
        """Extracts data from decoded serial input.

        All data in line is split by commas and put into array. Last item (CHECKSUM) is ignored 

        :param serial_data: serial data to extract
        :return: list of serial data, None if data not in expected format
        """
        serial_list = serial_data.split(",")

        # Time and CHECKSUM not included in active_parameters
        nbr_of_serial_parameters = len(self.active_parameters) + 2

        if len(serial_list) != nbr_of_serial_parameters:
            print("ERROR: Invalid number of parameters "
                  f"(Expected={len(serial_list)}, Actual={nbr_of_serial_parameters})")
            extracted_data_list = None
        else:
            extracted_data_list = []

            for parameter_idx, parameter in enumerate(serial_list[:-2]):
                # TODO Implement scaling into settings
                # extracted_data_list.append(float(parameter) * self.active_parameters[parameter_idx].unit_scale)
                extracted_data_list.append(float(parameter))

            extracted_data_list.append(int(serial_list[-2]))

            # extracted_data_list.append(datetime.datetime.fromtimestamp(int(serial_list[-2])/1000.0))

        return extracted_data_list


if __name__ == '__main__':
    print("NOTE: Module should not be run as main")
