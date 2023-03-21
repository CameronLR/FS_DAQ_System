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


MAX_PARAMETERS = 4

GRAPH_Y_AXIS_LABEL = [0 for i in range(MAX_PARAMETERS)]


@dataclass
class DAQ_Dataclass():
    speed_fr: int
    speed_fl: int
    speed_rr: int
    speed_rl: int
    engine_rev: int
    damper_fr: int
    damper_fl: int
    damper_rr: int
    damper_rl: int
    gear: int
    steering_whl_pos: int
    gyro_x: int
    gyro_y: int
    gyro_z: int
    b_voltage: int
    throttle: int
    fuel_pressure: int

    def __init__(self, data_list):
        self.speed_fr = data_list[0]
        self.speed_fl = data_list[1]
        self.speed_rr = data_list[2]
        self.speed_rl = data_list[3]
        self.engine_rev = data_list[4]
        self.damper_fr = data_list[5]
        self.damper_fl = data_list[6]
        self.damper_rr = data_list[7]
        self.damper_rl = data_list[8]
        self.gear = data_list[9]
        self.steering_whl_pos = data_list[10]
        self.gyro_x = data_list[11]
        self.gyro_y = data_list[12]
        self.gyro_z = data_list[13]
        self.b_voltage = data_list[14]
        self.throttle = data_list[15]
        self.fuel_pressure = data_list[16]


class DataCollectorThread(QtCore.QThread):
    data_signal = QtCore.Signal(DAQ_Dataclass)

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
                    self.data_signal.emit(data)

    def run_crc(self, serial_data):
        return False

    def extract_data(self, serial_data):
        serial_list = serial_data.split(",")
        print()

        if len(serial_list) != MAX_PARAMETERS + 1:
            return None
        else:
            return DAQ_Dataclass(serial_list)

    def serial_listener():
        pass
