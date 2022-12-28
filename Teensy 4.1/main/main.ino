#include "main.h"
#include <stdlib.h>
#include <iostream>
#include <ESP32Time.h>
using namespace std;
#define SENSOR_BUFFER_SIZE 1000000

typedef struct {
  // the wheel speed in MPH
  int wheel_speed;
  // the engine revolutions in RPM
  int engine_revs;
  // the position of the damper extension in mm
  int damper_position;
  // the angular rotation of the steering wheel in degrees
  int steering_wheel_position;
  // the relative strain
  int strain;
  // gyro position in degrees
  int gyro_x;
  int gyro_y;
  int gyro_z;
  // battery in deci-volts
  int VBat;
  // throttle position in mm
  int throttle_position;
  // fuel pressure in pascals?
  int fuel_pressure;
  // program run time
  unsigned long program_time_millis;
} sensor_data;

sensor_data *sensor_buffer = (sensor_data *)malloc(sizeof(sensor_data) * SENSOR_BUFFER_SIZE);

int buffer_location = 0;

datetime_t *rtc_start_time = (datetime_t *)malloc(sizeof(datetime_t));

ESP32Time rtc(3600); // offset in seconds GMT+1

void setup() {
  //delay(3000);
  Serial.begin(115200);

  bool is_working = rtc.getMillis();

  if (!is_working) {
    // fail!
  }
}

void loop() {
  if (buffer_location >= SENSOR_BUFFER_SIZE) {
    SendData();
    buffer_location = 0;
  } else {
    delay(10);
  }

  unsigned long program_time_ms = millis();
  sensor_data *current_data = &sensor_buffer[buffer_location];
  current_data->wheel_speed = GetWheelSpeed();
  current_data->engine_revs = GetEngineRevs();
  current_data->damper_position = GetDamperPosition();
  current_data->steering_wheel_position = GetSteeringWheelPosition();
  current_data->strain = GetStrain();
  current_data->gyro_x = GetGyroX();
  current_data->gyro_y = GetGyroY();
  current_data->gyro_z = GetGyroZ();
  current_data->VBat = GetVBat();
  current_data->throttle_position = GetThrottlePosition();
  current_data->fuel_pressure = GetFuelPressure();



  // Wheel Speed = 123; RPM = 2220; Damper position = 1212

  // To print out wheel speed at the fith timeinterval
  // cout << current_data[5].wheel_speed;
}