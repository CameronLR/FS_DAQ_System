/**
 * @file
 * @brief A file that is documented.
 *
 * Detailed description, etc.
 *
 * We may want to split these into seperate files for each interfaces (e.g. analogue, i2c, spi...)
 *
 */

#include <Arduino.h>
#include "gpio.h"

#define REV_SENSOR_PIN 23

static WheelSpeed_s gpio_getWheelSpeed();
static daq_EngineRev_t gpio_getEngineRevs(uint32_t lastPoll_ms);
static DamperPos_S gpio_getDamperPosition();
static daq_GearPos_t gpio_getGearPosition();
static daq_SteeringWhlPos_t gpio_getSteeringWheelPosition();
static GyroData_s gpio_getGyro();
static daq_BatteryV_t gpio_getVBat();
static daq_ThrottlePos_t gpio_getThrottlePosition();
static daq_FuelPressure_t gpio_getFuelPressure();

static void gpio_engineRevInterrupt();

// Keeps track of the amount of revs between each call of updateSensorInfo
volatile unsigned int revCount;

    void
    gpio_init()
{
  // This it the interrupt to help read the rev counter, pin A9 
  attachInterrupt( digitalPinToInterrupt(REV_SENSOR_PIN), gpio_engineRevInterrupt, RISING);
  revCount = 0;

}

bool updateSensorInfo(sensorData_s *pSensorData)
{
    pSensorData->wheelSpeed_mph = gpio_getWheelSpeed();
    pSensorData->engineRev_rpm = gpio_getEngineRevs(pSensorData->time_ms);
    pSensorData->damperPos_mm = gpio_getDamperPosition();
    pSensorData->gearPos = gpio_getGearPosition();
    pSensorData->steeringWheelPos_degrees = gpio_getSteeringWheelPosition();
    pSensorData->gyro = gpio_getGyro();
    pSensorData->batteryVoltage_dV = gpio_getVBat();
    pSensorData->throttlePos_mm = gpio_getThrottlePosition();
    pSensorData->fuelPressure_pa = gpio_getFuelPressure();

    return false;
}

static WheelSpeed_s gpio_getWheelSpeed()
{
    WheelSpeed_s wheelSpeed = {};
    return wheelSpeed;
}

static daq_EngineRev_t gpio_getEngineRevs(uint32_t lastPoll_ms)
{
    // Amount of time since the last time this function was called
    uint32_t timeElapsed = (uint32_t)millis() - lastPoll_ms;
    // The average amount of time between each rev
    float timePerRev = (float)timeElapsed / (float)revCount;

    // So we get the amount of time for 1 rev, do 1/elapsedTime to get it in Hz. Then mulitply by 60 to get in rpm.
    uint32_t rpm = (int)((1.0 / timePerRev) * 60.0);

    // Reset the revCount back to 0 for the next time this funciton is called
    revCount = 0;

    return rpm;
}

static DamperPos_S gpio_getDamperPosition()
{
    DamperPos_S damperPos = {};
    return damperPos;
}

static daq_GearPos_t gpio_getGearPosition()
{
    return 0;
}

static daq_SteeringWhlPos_t gpio_getSteeringWheelPosition()
{
    return 0;
}

static GyroData_s gpio_getGyro()
{
    // gpio_gyro info will likely be retrieved from Arduino Nano
    GyroData_s gyro = {};
    return gyro;
}

static daq_BatteryV_t gpio_getVBat()
{
    return 0U;
}

static daq_ThrottlePos_t gpio_getThrottlePosition()
{
    return 0U;
}

static daq_FuelPressure_t gpio_getFuelPressure()
{
    return 0U;
}



static void gpio_engineRevInterrupt(){
    
    // One call of this function is equal to 2 engine revs
    revCount += 2;
}