import sys
from PySide6 import QtCore

import time
import serial

from enum import Enum
from dataclasses import dataclass

COM_PORT = 'COM5'


class Status(int, Enum):
    RUNNING = 1
    STOPPED = 2


class DAQ_DataPoints(int, Enum):
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
        self.status = Status.STOPPED

        try:
            self.serial = serial.Serial(COM_PORT, 115200, timeout=1)
        except serial.SerialException:
            print("ERROR: Could not open serial port")
            self.serial = None
        else:
            self.serial.close()

    def run(self):
        while (1):
            if self.status == Status.STOPPED:
                print("STATUS = STOPPED")
                # Make sure serial is kept clear?
                time.sleep(0.5)
            else:
                print("STATUS = RUNNING")
                self.run_running()
                # do some stuff here

    @QtCore.Slot(int)
    def status_signal_slot(self, status_sig):
        self.status = status_sig
        if self.status == Status.STOPPED:
            print("Stopping Data Collector")
            # Close Serial Port
            if self.serial != None:
                self.serial.close()
        elif self.status == Status.RUNNING:
            print("Starting Data Collector")
            # Open Serial Port
            if self.serial != None:
                print("Opening serial!")
                self.serial.open()
                self.serial.flush()

        else:
            print("ERROR: Invalid status")
            self.status = Status.STOPPED

    def run_running(self):
        serial_data = "a"

        while serial_data != None and self.serial != None and self.serial.is_open != False and self.serial._overlapped_read != None:
            serial_data = self.serial.readline()
            serial_data = serial_data.decode("utf-8")

            crc_error = self.run_crc(serial_data)

            if not crc_error:
                data = self.extract_data(serial_data)

                if data != None:
                    print("Sending data")
                    self.data_signal.emit(data)

    def run_crc(self, serial_data):
        return False

    def extract_data(self, serial_data):
        serial_list = serial_data.split(",")
        print()

        if len(serial_list) != DAQ_DataPoints.END + 1:
            print("ERROR: Invalid number of parameters")
            return None
        else:
            list = []
            for i in range(len(serial_list)-1):
                list.append(int(serial_list[i]))
            return list

    def serial_listener():
        pass
