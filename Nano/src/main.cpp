/**
 * @file
 * @brief A file that is documented.
 *
 * Detailed description, etc.
 */

#include <Arduino.h>

#include "../../cmn/daq_common.h"
#include "server/server.h"
#include "gyro/gyro.h"
#include "nti/nti.h"
#include "ndi/ndi.h"

// Ideally we need to sync RTC on start up if we are using nano's gryoscope

const uint32_t NANO_SLEEP_MS = 10;

sensorData_s sensorData = {};

void setup()
{
    Serial.begin(115200);
    networkSetup();
}

void loop()
{
    if (Serial.available() > 0)
    {
        getDataFromTeensy(&sensorData);

        if (0U == sensorData.gyro.x)
        {
            sensorData.gyro = getGyro();
        }

        uploadDataToServer(&sensorData);
        sendDataToDisplay(&sensorData);
    }
    else
    {
        delay(NANO_SLEEP_MS);
    }
}