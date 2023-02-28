#ifndef DAQ_COMMON_H
#define DAQ_COMMON_H

#include <stdint.h>

typedef int32_t daq_WheelSpeed_t;
typedef int32_t daq_EngineRev_t;
typedef int32_t daq_DamperPos_t;
typedef int32_t daq_GearPos_t;
typedef int32_t daq_SteeringWhlPos_t;
typedef int32_t daq_Strain_t;
typedef int32_t daq_BatteryV_t;
typedef int32_t daq_ThrottlePos_t;
typedef int32_t daq_FuelPressure_t;

typedef struct GyroData_s
{
  int32_t x;
  int32_t y;
  int32_t z;
} GyroData_s;

typedef struct sensorData_s
{
  // the wheel speed in MPH
  daq_WheelSpeed_t wheelSpeed_mph;
  // the engine revolutions in RPM
  daq_EngineRev_t engineRev_rpm;
  // the position of the damper extension in mm
  daq_DamperPos_t damperPos_mm;
  // the gear number the car is currently in
  daq_GearPos_t gearPos;
  // the angular rotation of the steering wheel in degrees
  daq_SteeringWhlPos_t steeringWheelPos_degrees;
  // the relative strain
  daq_Strain_t strain;
  // gyro position in degrees
  GyroData_s gyro;
  // battery in deci-volts
  daq_BatteryV_t batteryVoltage_dV;
  // throttle position in mm
  daq_ThrottlePos_t throttlePos_mm;
  // fuel pressure in pascals?
  daq_FuelPressure_t fuelPressure_pa;
  // program run time
  unsigned long time_ms;
} sensorData_s;

#endif