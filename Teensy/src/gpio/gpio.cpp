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
    // Defining pins //
    #include <Arduino.h>

    float exten1, exten2, exten3, exten4;
    float DampPos1, DampPos2, DampPos3, DampPos4;

    // Initialising transmission //
    Serial.begin(9600);

    // Reading the voltage outputs //

    exten1 = analogRead(PIN_A0);
    exten2 = analogRead(PIN_A1);
    exten3 = analogRead(PIN_A2);
    exten4 = analogRead(PIN_A3);

    // Calibrating outputs to damper position //

    DampPos1 = (64 - exten1)/63000;
    DampPos2 = (64 - exten2)/63000;
    DampPos3 = (64 - exten3)/63000;
    DampPos4 = (64 - exten4)/63000;


    return (DampPos1, DampPos2, DampPos3, DampPos4);
}

static int32_t gpio_getGearPosition()
{
    return 0;
}

static uint32_t gpio_getSteeringWheelPosition()
{
    #include <Wire.h>
    #include <Arduino.h>
   const int MPU = 0x68; //MPU6050 I2C Address
   float AccX, AccY, AccZ;
   float GyroX, GyroY, GyroZ;
   float gyroAngleX, gyroAngleY, gyroAngleZ;
   float elapsedTime, currentTime, previousTime;
   float startPosX, startPosY, startPosZ;
   float currentPosX, currentPosY, currentPosZ;
   float yaw;
   float calibrationvalue;
   int c = 0;


    Serial.begin(19200);
    Wire.begin();
    Wire.beginTransmission(MPU);
    Wire.write(0x6B);
    Wire.write(0x00);
    Wire.endTransmission(true);
    delay(20);


    // Setting starting position of the sensor //

    startPosX = 0;
    startPosY = 0;
    startPosZ = 0;

    // Reading Gyroscope data //

    previousTime = currentTime;
    currentTime = millis();
    elapsedTime = (currentTime - previousTime)/1000; //Outputs the elapsed time in seconds

    Wire.beginTransmission(MPU);
    Wire.write(0x43); //Starts transmission with Gyroscope output
    Wire.endTransmission(false);
    Wire.requestFrom(MPU,6,true);

    calibrationvalue = 16.375; // Value is the raw value divided by the transformation to get to a range 2000 deg

    GyroX = (Wire.read() << 8 | Wire.read()) / calibrationvalue; //Reading the Gyro values and then calibrating them to match the range of the Gyro
    GyroY = (Wire.read() << 8 | Wire.read()) / calibrationvalue;
    GyroZ = (Wire.read() << 8 | Wire.read()) / calibrationvalue;

    yaw = yaw + GyroZ*elapsedTime; //Calculating value for steering Yaw

    // Possibly include a section calculating error in the values //

    // Possibly return a series of Gyro positions over time //


    return (yaw);
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
