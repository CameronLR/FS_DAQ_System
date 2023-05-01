#ifndef DAQ_COMMON_H
#define DAQ_COMMON_H

#include <stdint.h>

typedef int32_t daq_EngineRev_t;
typedef int32_t daq_DamperPos_t;
typedef int32_t daq_GearPos_t;
typedef int32_t daq_SteeringWhlPos_t;
typedef int32_t daq_Strain_t;
typedef uint32_t daq_BatteryV_t;
typedef int32_t daq_ThrottlePos_t;
typedef int32_t daq_FuelPressure_t;
typedef int32_t daq_GPSVehicleSpeed_t;

typedef struct WheelSpeed_s
{
  int32_t fr; // Front Right
  int32_t fl; // Front Left
  int32_t rr; // Rear Right
  int32_t rl; // Rear Left
} WheelSpeed_s;

typedef struct DamperPos_S
{
  int32_t fr; // Front Right
  int32_t fl; // Front Left
  int32_t rr; // Rear Right
  int32_t rl; // Rear Left
} DamperPos_S;
typedef struct GyroData_s
{
  int32_t x;
  int32_t y;
  int32_t z;
} GyroData_s;

typedef struct sensorData_s
{
  // the wheel speed in MPH
  WheelSpeed_s wheelSpeed_mph;
  // the engine revolutions in RPM
  daq_EngineRev_t engineRev_rpm;
  // the position of the damper extension in mm
  DamperPos_S damperPos_mm;
  // the gear number the car is currently in
  daq_GearPos_t gearPos;
  // the angular rotation of the steering wheel in degrees
  daq_SteeringWhlPos_t steeringWheelPos_degrees;
  // gyro position in degrees
  GyroData_s gyro;
  // battery in deci-volts
  daq_BatteryV_t batteryVoltage_dV;
  // throttle position in mm
  daq_ThrottlePos_t throttlePos_mm;
  // fuel pressure in pascals?
  daq_FuelPressure_t fuelPressure_pa;
  // vehicle speed using GPS
  daq_GPSVehicleSpeed_t GPSVehicleSpeed;
  // program run time
  uint32_t time_ms;
} sensorData_s;

#endif