/**
 * @file
 * @brief A file that is documented.
 *
 * Detailed description, etc.
 */


#include <Arduino.h>
#include <SD.h>
#include <SPI.h>
#include <TimeLib.h>
#include <DS1307RTC.h>

#include "sdCard.h"

File dataFile;
String timeStamp;
char * fileName;
const int chipSelect = BUILTIN_SDCARD;


extern bool sendDataToSdCard(sensorData_s *pSensorData)
{

fileName = (char*) timeStamp.c_str();
dataFile = SD.open(fileName, FILE_WRITE);

  //if there was no problem opening the file => write to it
  if (dataFile) {
    Serial.print("writing to");
    Serial.println(fileName);
    
    //Print the data to the file
    dataFile.print(String(pSensorData->wheelSpeed_mph.fr) + ",");
    dataFile.print(String(pSensorData->wheelSpeed_mph.fl) + ",");
    dataFile.print(String(pSensorData->wheelSpeed_mph.rr) + ",");
    dataFile.print(String(pSensorData->wheelSpeed_mph.rl) + ",");

    dataFile.print(String(pSensorData->engineRev_rpm) + ",");

    dataFile.print(String(pSensorData->damperPos_mm.fr) + ",");
    dataFile.print(String(pSensorData->damperPos_mm.fl) + ",");
    dataFile.print(String(pSensorData->damperPos_mm.rr) + ",");
    dataFile.print(String(pSensorData->damperPos_mm.rl) + ",");

    dataFile.print(String(pSensorData->gearPos) + ",");

    dataFile.print(String(pSensorData->steeringWheelPos_degrees) + ",");

    dataFile.print(String(pSensorData->gyro.x) + ",");
    dataFile.print(String(pSensorData->gyro.y) + ",");
    dataFile.print(String(pSensorData->gyro.z) + ",");

    dataFile.print(String(pSensorData->batteryVoltage_dV) + ",");

    dataFile.print(String(pSensorData->throttlePos_mm) + ",");

    dataFile.print(String(pSensorData->fuelPressure_pa) + ",");

    dataFile.println(String(pSensorData->time_ms) + ",");

    dataFile.close();
  } else {
    //if the file couldn't be opend => print error message
    Serial.print("error oppening the file :");
    Serial.println(fileName); 
  }
    return true;
}


extern bool sdCard_init() 
{

  //Get the time to use for a timestamp
  timeStamp = String("FS_DAQ_Log_" + String(year()) + "-" + String(month())\
  + "-" + String(day()) + "-" + String(hour()) + ":" + String(minute())\
  + ":" + String(second()) + ".csv");

  Serial.print("Initializing SD card...");

  if (!SD.begin(chipSelect)) {
    Serial.println("Initialization failed!");
    return false;
  }
  Serial.println("Initialization SD card done.");

  fileName = (char*) timeStamp.c_str();
  dataFile = SD.open(fileName, FILE_WRITE);

  if (dataFile) {
    Serial.print("writing to");
    Serial.println(fileName);
    
    //Print the data to the file
    dataFile.print("Wheel Speed FR (mph),");
    dataFile.print("Wheel Speed FL (mph),");
    dataFile.print("Wheel Speed RR (mph),");
    dataFile.print("Wheel Speed RL (mph),");

    dataFile.print("Engine Revs (rpm),");

    dataFile.print("Damper Position FR (mm),");
    dataFile.print("Damper Position FL (mm),");
    dataFile.print("Damper Position RR (mm),");
    dataFile.print("Damper Position RL (mm),");

    dataFile.print("Gear Position,");

    dataFile.print("Steering Wheel Position (Degrees),");

    dataFile.print("Gryo X Position (Degrees),");
    dataFile.print("Gryo Y Position (Degrees),");
    dataFile.print("Gryo Z Position (Degrees),");

    dataFile.print("Battery Voltage (dV)");

    dataFile.print("Throttle Position (mm),");

    dataFile.print("Fuel Pressure (Pa),");
    
    dataFile.println("Run Time (ms),");

    dataFile.close();
  } else {

    //if the file couldn't be opend => print error message
    Serial.print("error oppening the file :");
    Serial.println(fileName); 
    return false;
  }

  return true;
}


//Not sure if the Serial will work withought passing it between files 
//Could have more Error messages/ handling