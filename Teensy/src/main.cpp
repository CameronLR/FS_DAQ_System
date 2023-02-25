/**
 * @file
 * @brief A file that is documented.
 *
 * Detailed description, etc.
 */

#include <Arduino.h>
#include <TimeLib.h>
#include <DS1307RTC.h>
#include <SD.h>
#include <SPI.h>

#include "../../cmn/daq_common.h"
#include "gpio/gpio.h"
#include "sdCard/sdCard.h"
#include "tni/tni.h"

const int chipSelect = BUILTIN_SDCARD;

sensorData_s dataStruct = {};

static void sendUpdatedSensorInfo(sensorData_s *pSensorData, uint32_t currentTime_ms);

void setup()
{
  Serial.begin(115200);
  while (!Serial) {
    ; //wait for the serial to connect
  }

  setSyncProvider(RTC.get); // the function to get the time from the RTC

  if (timeStatus() != timeSet)
  {
    Serial.println("Unable to sync with the RTC");
  }
  else
  {
    Serial.println("RTC has set the system time");
  }

  Serial.print("Initializing SD card...");

  if (!SD.begin(chipSelect)) {
    Serial.println("Initialization failed!");
    return;
  }
  Serial.println("Initialization SD card done.");
}

void loop() 
{
  bool error = updateSensorInfo(&dataStruct);
  
  uint32_t currentTime_ms = millis();

  if (!error)
  {
    sendUpdatedSensorInfo(&dataStruct, currentTime_ms);
  }
}

static void sendUpdatedSensorInfo(sensorData_s *pSensorData, uint32_t currentTime_ms)
{
  if (NULL == pSensorData)
  {
    Serial.print("NULL PARAM");
  }
  else
  {
    sendDataToNano(pSensorData);
    sendDataToSdCard(pSensorData);
  }
}
