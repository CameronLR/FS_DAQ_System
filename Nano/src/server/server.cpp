/**
 * @file
 * @brief A file that is documented.
 *
 * Detailed description, etc.
 */

#include <Arduino.h>
#include "server.h"

void networkSetup()
{
    // Connect to wireless hotspot
}

void uploadDataToServer(sensorData_s *pSensorData)
{
    // Go through each piece of data in sensorData and send command to server
    // Add checksum to each piece of data
}