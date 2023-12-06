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
#include <math.h>

#define SIZE_OF_CIRCLE_ARRAY 10
#define REV_SENSOR_PIN 23
#define BATTERY_SENSOR_PIN A16

#define GEAR_SHIFT_UP_PIN 31 //CTX3
#define GEAR_SHIFT_DOWN_PIN 32 //OUT1B

#define NEUTRAL_TIME_MS 250
#define BUTTON_BOUNCE_THRESHOLD 150

#define FR_DAMPER_SENSOR_PIN A0 //Pin 14
#define FL_DAMPER_SENSOR_PIN A1 //Pin 15
#define RR_DAMPER_SENSOR_PIN A7 //Pin 21
#define RL_DAMPER_SENSOR_PIN A6 //Pin 20

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

static void gearUpShiftInterrupt();
static void gearDownShiftInterrupt();

volatile daq_GearPos_t gearPosition = 0;
volatile int lastGearUpdate = 0;
volatile int gearUpBtnStartTime = 0;

const int maxGear = 6;
const int minGear = 0;

    void
    gpio_init()
{
  // This it the interrupt to help read the rev counter, pin A9 
  attachInterrupt( digitalPinToInterrupt(REV_SENSOR_PIN), gpio_engineRevInterrupt, RISING);

  //Initializing the pins for the electronic shifter

  pinMode(GEAR_SHIFT_UP_PIN, INPUT_PULLDOWN);
  pinMode(GEAR_SHIFT_DOWN_PIN, INPUT_PULLDOWN);

  attachInterrupt(digitalPinToInterrupt(GEAR_SHIFT_UP_PIN),   gearUpShiftInterrupt, CHANGE);
  attachInterrupt(digitalPinToInterrupt(GEAR_SHIFT_DOWN_PIN),  gearDownShiftInterrupt , FALLING);

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

int32_t damperEquation(int32_t x) {
  /*
  This equation will give you the value of the actual extension, if you want to the measurement
  from the top bit of the potentiometer to the red line then you need to +29 onto the mm value you
  get from this equation.
  */
  int32_t value = round((-0.059*x+89.722)-28.94);
  return value;
}

static DamperPos_S gpio_getDamperPosition()
{
    /*
    Read and convert sensor value potentiometer (which should be a value from 0 to 1023 
    based on the voltage with 3.3v max) then use the damper equation calculate
    the mm extension value for the potentiometer using the sensor value, make sure the max value 
    for the sensor is 1023 (when the potentiometer is fully closed) and not anything below.
    */ 

    int32_t damperPosFRvalue = analogRead(FR_DAMPER_SENSOR_PIN);
    int32_t damperPosFLvalue = analogRead(FL_DAMPER_SENSOR_PIN);
    int32_t damperPosRRvalue = analogRead(RR_DAMPER_SENSOR_PIN);
    int32_t damperPosRLvalue = analogRead(RL_DAMPER_SENSOR_PIN);

    DamperPos_S damperPos = {};

    damperPos.fr = damperEquation(damperPosFRvalue);
    damperPos.fl = damperEquation(damperPosFLvalue);
    damperPos.rr = damperEquation(damperPosRRvalue);
    damperPos.rl = damperEquation(damperPosRLvalue);

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


//On a change of the Up pin if its been less than NEUTRAL_TIME_MS since the RISING interupt, then its in neutral, 
static void gearUpShiftInterrupt() 
{
    int gearShiftUpPinState = digitalRead(GEAR_SHIFT_UP_PIN);

    if (gearShiftUpPinState == 1) { //If NO then make this 1

        //It is FALLING interupt
        gearUpBtnStartTime = millis();

    } else {

        //It is RISING interupt
        if ((millis() - gearUpBtnStartTime) < NEUTRAL_TIME_MS && ((millis() - lastGearUpdate) > BUTTON_BOUNCE_THRESHOLD)) {
        
            lastGearUpdate = millis();
		    gearPosition = 0;

        } else if ((millis() - lastGearUpdate) > BUTTON_BOUNCE_THRESHOLD)
        {
            gearPosition = (gearPosition + 1 > maxGear) ? maxGear : gearPosition + 1;
            lastGearUpdate = millis();
        } 
    } 
}

//If FALLING detected then shift the gear down one (when the button is released)
static void gearDownShiftInterrupt()
{

    if ((millis() - lastGearUpdate) > BUTTON_BOUNCE_THRESHOLD)
    {
        gearPosition = (gearPosition - 1 < minGear) ? minGear : gearPosition - 1;
        lastGearUpdate = millis();
        
    }

}
