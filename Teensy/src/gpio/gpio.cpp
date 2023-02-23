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

static int32_t gpio_getWheelSpeed();
static uint32_t gpio_getEngineRevs();
static int32_t gpio_getDamperPosition();
static int32_t gpio_getGearPosition();
static uint32_t gpio_getSteeringWheelPosition();
static int32_t gpio_getStrain();
static GyroData_s gpio_getGyro();
static uint32_t gpio_getVBat();
static uint32_t gpio_getThrottlePosition();
static uint32_t gpio_getFuelPressure();

bool updateSensorInfo(sensorData_s *pSensorData)
{
    pSensorData->wheel_speed = gpio_getWheelSpeed();
    pSensorData->engine_revs = gpio_getEngineRevs();
    pSensorData->damper_position = gpio_getDamperPosition();
    pSensorData->gear_position = gpio_getGearPosition();
    pSensorData->steering_wheel_position = gpio_getSteeringWheelPosition();
    pSensorData->strain = gpio_getStrain();
    pSensorData->gyro = gpio_getGyro();
    pSensorData->VBat = gpio_getVBat();
    pSensorData->throttle_position = gpio_getThrottlePosition();
    pSensorData->fuel_pressure = gpio_getFuelPressure();

    return false;
}

static int32_t gpio_getWheelSpeed()
{
    return 0;
}

static uint32_t gpio_getEngineRevs()
{
    return 0U;
}

static int32_t gpio_getDamperPosition()
{
    return 0;
}

static int32_t gpio_getGearPosition()
{
    return 0;
}

static uint32_t gpio_getSteeringWheelPosition()
{
    return 0;
}

static int32_t gpio_getStrain()
{
    return 0;
}

static GyroData_s gpio_getGyro()
{
    // gpio_gyro info will likely be retrieved from Arduino Nano
    GyroData_s gyro = {};
    return gyro;
}

static uint32_t gpio_getVBat()
{
    return 0U;
}

static uint32_t gpio_getThrottlePosition()
{
    return 0U;
}

static uint32_t gpio_getFuelPressure()
{
    return 0U;
}
