#ifndef DAQ_COMMON_H
#define DAQ_COMMON_H

#include <stdint.h>

typedef struct GyroData_s
{
  int32_t x;
  int32_t y;
  int32_t z;
} GyroData_s;

typedef struct sensorData_s
{
  // the wheel speed in MPH
  int wheel_speed;
  // the engine revolutions in RPM
  int engine_revs;
  // the position of the damper extension in mm
  int damper_position;
  // the gear number the car is currently in
  int gear_position;
  // the angular rotation of the steering wheel in degrees
  int steering_wheel_position;
  // the relative strain
  int strain;
  // gyro position in degrees
  GyroData_s gyro;
  // battery in deci-volts
  int VBat;
  // throttle position in mm
  int throttle_position;
  // fuel pressure in pascals?
  int fuel_pressure;
  // program run time
  unsigned long program_time_millis;
} sensorData_s;

#endif