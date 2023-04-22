################################################################################
# DataCollector Python File
#
#
#
################################################################################
import time
import datetime
from enum import Enum


import serial

from PySide6 import QtCore


DEFAULT_SERIAL_PORT = 'COM10'
SERIAL_PORT_BAUD = 115200


class CollectorStatus(int, Enum):
    """Enum representing the data collector's state"""
    RUNNING = 1
    STOPPED = 2


class FsDaqData(int, Enum):
    """Enum representing the DAQ data points index received through serial port"""
    WHL_SPEED_FR = 0
    WHL_SPEED_FL = 1
    WHL_SPEED_RR = 2
    WHL_SPEED_RL = 3
    ENGINE_REVS = 4
    DAMPER_POS_FR = 5
    DAMPER_POS_FL = 6
    DAMPER_POS_RR = 7
    DAMPER_POS_RL = 8
    GEAR_POS = 9
    STR_WHL_POS = 10
    GYRO_X = 11
    GYRO_Y = 12
    GYRO_Z = 13
    BAT_VOLT = 14
    THROTTLE = 15
    FUEL_PRESSURE = 16
    TIME = 17
    END = 18


class DataCollectorThread(QtCore.QThread):
    data_signal = QtCore.Signal(object)

    def __init__(self, parent):
        super(DataCollectorThread, self).__init__(parent=parent)
        self.status = CollectorStatus.STOPPED

        self.start_time = 0

        try:
            self.serial = serial.Serial(DEFAULT_SERIAL_PORT, SERIAL_PORT_BAUD, timeout=1)
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
        while (1):
            if self.status == CollectorStatus.STOPPED:
                # TODO find out if we need to keep flushing here to keep serial buffer clear
                time.sleep(0.5)
            else:
                self.listen()

    @QtCore.Slot(str)
    def set_serial_port(self, serial_port):
        """Qt Slot to set serial port of DataCollector
        :param serial_port: str: serial port name to open
        """
        if self.serial.is_open:
            self.serial.close()

        try:
            self.serial = serial.Serial(serial_port, SERIAL_PORT_BAUD, timeout=1)
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

    def listen(self):
        """ Keeps processing and posting serial data until serial port is free
        """
        serial_data = " "

        while self.serial is not None and self.serial.is_open and \
                self.serial._overlapped_read is not None:  # pylint: disable=W0212
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
        _ = serial_data
        return True

    def extract_data(self, serial_data):
        """Extracts data from decoded serial input.

        All data in line is split by commas and put into array. Last item (CHECKSUM) is ignored 

        :param serial_data: serial data to extract
        :return: list of serial data, None if data not in expected format
        """
        serial_list = serial_data.split(",")

        if len(serial_list) != FsDaqData.END + 1:
            print("ERROR: Invalid number of parameters")
            extracted_data_list = None
        else:
            extracted_data_list = [int(data_item) for data_item in serial_list[:-2]]
            # extracted_data_list.append(datetime.datetime.fromtimestamp(int(serial_list[-2])/1000.0))
            extracted_data_list.append(int(serial_list[-2]))

        return extracted_data_list
