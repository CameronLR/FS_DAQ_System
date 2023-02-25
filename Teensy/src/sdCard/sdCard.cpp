/**
 * @file
 * @brief A file that is documented.
 *
 * Detailed description, etc.
 */


#include <Arduino.h>
#include <SD.h>
#include <SPI.h>
#include "sdCard.h"

File dataFile;
const char * fileName = "data.csv";

extern bool sendDataToSdCard(sensorData_s *pSensorData)
{
dataFile = SD.open(fileName, FILE_WRITE);

  //if there was no problem opening the file => write to it
  if (dataFile) {
    Serial.print("writing to");
    Serial.println(fileName);
    
    //Print the data to the file
    dataFile.print(pSensorData->wheel_speed);
    dataFile.print(pSensorData->engine_revs);
    dataFile.print(pSensorData->damper_position);
    dataFile.print(pSensorData->gear_position);
    dataFile.print(pSensorData->steering_wheel_position);
    dataFile.print(pSensorData->strain);
    dataFile.print(pSensorData->gyro.x);
    dataFile.print(pSensorData->gyro.y);
    dataFile.print(pSensorData->gyro.z);
    dataFile.print(pSensorData->VBat);
    dataFile.print(pSensorData->throttle_position);
    dataFile.print(pSensorData->fuel_pressure);
    dataFile.println(pSensorData->program_time_millis);

    dataFile.close();
  } else {
    //if the file couldn't be opend => print error message
    Serial.print("error oppening the file :");
    Serial.println(fileName); 
  }
    return true;
}