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
#define SIZE_OF_CIRCLE_ARRAY 10
#define REV_SENSOR_PIN 23
#define BATTERY_SENSOR_PIN A16

static WheelSpeed_s gpio_getWheelSpeed();
static daq_EngineRev_t gpio_getEngineRevs();
static DamperPos_S gpio_getDamperPosition();
static daq_GearPos_t gpio_getGearPosition();
static daq_SteeringWhlPos_t gpio_getSteeringWheelPosition();
static GyroData_s gpio_getGyro();
static daq_BatteryV_t gpio_getVBat();
static daq_ThrottlePos_t gpio_getThrottlePosition();
static daq_FuelPressure_t gpio_getFuelPressure();

static void gpio_engineRevInterrupt();

// Keeps track of the amount of revs between each call of updateSensorInfo
volatile int revCount[SIZE_OF_CIRCLE_ARRAY];
volatile int revPosition = 0;

    void
    gpio_init()
{
  // This it the interrupt to help read the rev counter, pin A9 
  attachInterrupt( digitalPinToInterrupt(REV_SENSOR_PIN), gpio_engineRevInterrupt, RISING);

}

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
    pSensorData->time_ms = millis();
    return false;
}

static WheelSpeed_s gpio_getWheelSpeed()
{
    WheelSpeed_s wheelSpeed = {};
    return wheelSpeed;
}

static daq_EngineRev_t gpio_getEngineRevs()
{
    int end = revCount[(revPosition +SIZE_OF_CIRCLE_ARRAY -1) % SIZE_OF_CIRCLE_ARRAY];
    int start = revCount[revPosition];

    float timePerRev = (float)(end - start) / (SIZE_OF_CIRCLE_ARRAY-1) / 1000000.0;

    // So we get the amount of time for 1 rev, do 1/elapsedTime to get it in Hz. Then mulitply by 60 to get in rpm.
    int32_t rpm = (int32_t)((1.0 / timePerRev) * 2.0 * 60.0);

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

#define GX 0x37
float fGyro[3];
static GyroData_s gpio_getGyro()
{
    for(int i = 0; i < 3; i++){
        fGyro[i] = GX+i / 32768.0f * 2000.0f;
        fGyro[i] = (int32_t)fGyro[i];
    }
    GyroData_s gyro = {fGyro[1], fGyro[2], fGyro[3]};   
    return gyro;
}

// defining resistors for voltage divider
constexpr float BATTERY_SCALAR = (4000.0f + 1000.0f ) / 1000.0f;
// the ADC analog input is returned in 10 bit format 
#define ADC_MAX_VALUE 1023
// the ADC can only handle 3.3V
#define ADC_MAX_VOLTAGE 3.3
static daq_BatteryV_t gpio_getVBat()
{
    float batteryAnalogIn = analogRead(BATTERY_SENSOR_PIN);
    // the formula for 2 resistors connected in series, forming the voltage divider is: V1 = Vm * (R2/(R1+R2))
    daq_BatteryV_t batteryVoltage_dV = (daq_BatteryV_t) ((batteryAnalogIn /
    ADC_MAX_VALUE) * ADC_MAX_VOLTAGE) * BATTERY_SCALAR * 10;
    
    return batteryVoltage_dV;
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
    
    revCount[revPosition] = micros();
    revPosition = (revPosition+1) % SIZE_OF_CIRCLE_ARRAY;
}