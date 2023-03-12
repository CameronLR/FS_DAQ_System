/**
 * @file
 * @brief SD card handling functions.
 *
 * implementing the sdCard functionality.
 * sdCard_appendLine function that send data from the sensors and stores them in the sd card.
 * sdCard_init function that initializes and timestamps the sdCard and file within it.
 *
 */

#include <Arduino.h>
#include <SD.h>
#include <SPI.h>
#include <TimeLib.h>
#include <DS1307RTC.h>
#include "sdCard.h"

#define FILENAME_LEN 40
static char gFilename[FILENAME_LEN];

bool gSdCardError = false;

const int chipSelect = BUILTIN_SDCARD;

bool sdCard_init()
{
  /**
   * \return result - true if init was successful, else false
   * \details
   *      Function first uses the Time library to create a timestamp as a filename for
   *      the csv file that will be on the sd card and opens it, creating it if it doesnt exist.
   *      Then writes headers for the sensor data esentially telling us what is on the sd
   *      card.
   *      Also prints errors to the Serial if they occour.
   */

  // Formats csv file's name with current time
  snprintf(gFilename, FILENAME_LEN, "FS_DAQ_Log_%d-%d-%d_%d-%d-%d.csv", year(), month(), day(), hour(), minute(), second());

  Serial.println("Initializing SDCARD ...");

  if (!SD.begin(chipSelect))
  {
    Serial.println("ERROR: Unable to connect to SDCARD");
    return false;
  }
  Serial.println("SDCARD initialisation successful");

  File dataFile = SD.open(gFilename, FILE_WRITE);
  if (!dataFile)
  {
    Serial.print("ERROR: could not open file: ");
    Serial.println(gFilename);
    return false;
  }

  Serial.print("Writing to: ");
  Serial.println(gFilename);

  // Set-up file with data headers
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

  dataFile.print("Battery Voltage (dV),");

  dataFile.print("Throttle Position (mm),");

  dataFile.print("Fuel Pressure (Pa),");

  dataFile.println("Run Time (ms),");

  dataFile.close();

  Serial.println("FS_DAQ_Log initialised successfully");

  return true;
}

bool sdCard_appendLine(sensorData_s *pSensorData)
{
  /**
   * \param[in] pSensorData pointer to sensor data to append to csv file
   * \return result - true if write was successful, else false
   * \details
   *      function recives a pointer to sensordata, it opens the File on the sd card
   *      that will have been created in the initialsation function. Then prints to the file
   *      on the sd card and closes it.
   *      Also prints errors to the Serial if they occour.
   */
  File dataFile = SD.open(gFilename, FILE_WRITE);

  if (!dataFile)
  {
    // if write has not failed before output error message
    if (!gSdCardError)
    {
      gSdCardError = true;
      Serial.print("ERROR: could not open file: ");
      Serial.println(gFilename);
    }
  }
  else
  {
    // if there was no problem opening the file => write to it
    gSdCardError = false;
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
  }

  return gSdCardError;
}
