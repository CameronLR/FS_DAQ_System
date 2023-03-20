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

#define GEAR_SHIFT_UP_PIN 2
#define GEAR_SHIFT_DOWN_PIN 3

static WheelSpeed_s gpio_getWheelSpeed();
static daq_EngineRev_t gpio_getEngineRevs();
static DamperPos_S gpio_getDamperPosition();
static daq_GearPos_t gpio_getGearPosition();
static daq_SteeringWhlPos_t gpio_getSteeringWheelPosition();
static GyroData_s gpio_getGyro();
static daq_BatteryV_t gpio_getVBat();
static daq_ThrottlePos_t gpio_getThrottlePosition();
static daq_FuelPressure_t gpio_getFuelPressure();

bool updateSensorInfo(sensorData_s *pSensorData)
{
    pSensorData->wheelSpeed_mph = gpio_getWheelSpeed();
    pSensorData->engineRev_rpm = gpio_getEngineRevs();
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

static daq_EngineRev_t gpio_getEngineRevs()
{
    return 0U;
}

static DamperPos_S gpio_getDamperPosition()
{
    DamperPos_S damperPos = {};
    return damperPos;
}

static daq_GearPos_t gpio_getGearPosition()
{
    /**
    * \return result - returns the int value of gear position
    * \details
    *         Gear 1, is when the car is fully shifted down
    *         Neutral, is one shift up from gear 1
    *         Gear 2, is a shift up from neutral
    *         Gear 3, is a shift up from gear 2
    *         
    *         Max gear = 6.
    */


    daq_GearPos_t gearPosition = 0;
    int up_shift_state = digitalRead(GEAR_SHIFT_DOWN_PIN);
    int down_shift_state = digitalRead(GEAR_SHIFT_UP_PIN);

    const int max_gear = 6;
    const int min_gear = 0;

    if (up_shift_state == HIGH) {
        gearPosition = (gearPosition + 1 > max_gear) ? max_gear : gearPosition + 1;
    }

    if (down_shift_state == HIGH) {
        gearPosition = (gearPosition - 1 < min_gear) ? min_gear : gearPosition - 1;
    }

    return gearPosition;
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

void gpio_init()
{
    //Initializing the pins for the hall effect sensors
    pinMode(GEAR_SHIFT_UP_PIN, INPUT);
    pinMode(GEAR_SHIFT_DOWN_PIN, INPUT);

}