/**
 * @file
 * @brief A file that is documented.
 *
 * Detailed description, etc.
 */

#include <Arduino.h>
#include "tni.h"

bool sendDataToNano(sensorData_s *pSensorData)
{
    /**
    * \return result - true if sending was successful, else false
    * \details
    *      Function that sends the sensordata to the Arduino Nano
    *      Uses Serial1 to communicate between them
    */

    Serial1.print(String(pSensorData->wheelSpeed_mph.fl) + ",");
    Serial1.print(String(pSensorData->wheelSpeed_mph.fr) + ",");
    Serial1.print(String(pSensorData->wheelSpeed_mph.rr) + ",");
    Serial1.print(String(pSensorData->wheelSpeed_mph.rl) + ",");

    Serial1.print(String(pSensorData->engineRev_rpm) + ",");

    Serial1.print(String(pSensorData->damperPos_mm.fr) + ",");
    Serial1.print(String(pSensorData->damperPos_mm.fl) + ",");
    Serial1.print(String(pSensorData->damperPos_mm.rr) + ",");
    Serial1.print(String(pSensorData->damperPos_mm.rl) + ",");

    Serial1.print(String(pSensorData->gearPos) + ",");

    Serial1.print(String(pSensorData->steeringWheelPos_degrees) + ",");

    Serial1.print(String(pSensorData->gyro.x) + ",");
    Serial1.print(String(pSensorData->gyro.y) + ",");
    Serial1.print(String(pSensorData->gyro.z) + ",");

    Serial1.print(String(pSensorData->batteryVoltage_dV) + ",");

    Serial1.print(String(pSensorData->throttlePos_mm) + ",");

    Serial1.print(String(pSensorData->fuelPressure_pa) + ",");

    Serial1.println(String(pSensorData->time_ms) + ",");
  
    return true;
}
