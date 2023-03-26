/**
 * @file
 * @brief A file that is documented.
 *
 * Detailed description, etc.
 */

#include <Arduino.h>
#include <SoftwareSerial.h>
#include "tni.h"
#include "Nextion.h"

// Declare Nextion objects - (page_id, component_id, component_name) 
NexNumber nRevs = NexNumber(0, 1, "nRevs");
NexNumber nBat = NexNumber(0, 2, "nBat");
NexNumber nGear = NexNumber(0, 3, "nGear");
NexNumber nSpeed = NexNumber(0, 4, "nSpeed");

bool nextion_init() 
{
    /**
    * \return result - true if init was successful, else false
    * \details
    *      Function initializes the Nextion using Nextion.h library, 
    *      may need to edit the NextionConfig.h file to get the correct serial atm
    *      it is Serial2 
    */

    nexInit();
    return 1; 
}


bool sendDataToNextion(sensorData_s *pSensorData)
{
    /**
    * \param[in] pSensorData pointer to sensor data to append to csv file
    * \return result - true if write was successful, else false
    * \details
    *      function recives a pointer to sensordata, it then 
    *      sends the data To display by updating their values, for wheel speed
    *      it takes an average
    */
    
    nRevs.setValue(pSensorData->engineRev_rpm);

    nBat.setValue(pSensorData->batteryVoltage_dV);

    nGear.setValue(pSensorData->gearPos);

    //calculate the average speed from the four wheels
    int totalWheelSpeed;

    totalWheelSpeed += pSensorData->wheelSpeed_mph.fr;
    totalWheelSpeed += pSensorData->wheelSpeed_mph.fl;
    totalWheelSpeed += pSensorData->wheelSpeed_mph.rr;
    totalWheelSpeed += pSensorData->wheelSpeed_mph.rl;

    nSpeed.setValue(totalWheelSpeed/4);

    return 1;
}
