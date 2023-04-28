/**
 * @file RF Module handling functions.
 * @brief 
 * 
 *  functions to setup and transmit data from teensey, sets the nrf24l01 module
 *  as a transmitter.
 *  
 *
 *
 */

#include <Arduino.h>
#include <SPI.h>
#include "rfModule.h"

#include "RF24.h"
#include "nRF24L01.h" 

#define CE_PIN 9 //Theese can be any
#define CSN_PIN 10 

// MOSI: - pin 11 
// MISO: - pin 12
// SCK: - pin 13

RF24 radio(CE_PIN, CSN_PIN);
const byte address[6] = "00001";
const byte checksum = 0;
const char newline = '\n';

bool rfModule_init() 
{

    if (!radio.begin()) {
        //may need to wait here
        Serial.println("ERROR: Unable to connect to rfModule");
        return false;
    }

    radio.setDataRate(RF24_250KBPS);           // greater = more distance
    radio.setPALevel(RF24_PA_MAX);             // alternative is RF24_PA_LOW.
    
    radio.setPayloadSize(4);                   //set size of what is being sent (32 max) 4 or 32
    radio.openWritingPipe(address);            //Set to TX
    radio.stopListening();

    // could send it ints at a time i.e 4 bytes at a time or as 32 byte chunks
    


    return true;
}


bool rfModule_sendline(sensorData_s *pSensorData)
{
    //write the data using pointers to sensor data + checksum + newline
    radio.write(&pSensorData->wheelSpeed_mph.fr, sizeof(pSensorData->wheelSpeed_mph.fr)); 
    radio.write(&pSensorData->wheelSpeed_mph.fl, sizeof(pSensorData->wheelSpeed_mph.fl)); 
    radio.write(&pSensorData->wheelSpeed_mph.rr, sizeof(pSensorData->wheelSpeed_mph.rr)); 
    radio.write(&pSensorData->wheelSpeed_mph.rl, sizeof(pSensorData->wheelSpeed_mph.rl)); 

    radio.write(&pSensorData->engineRev_rpm, sizeof(pSensorData->engineRev_rpm)); 

    radio.write(&pSensorData->damperPos_mm.fr, sizeof(pSensorData->damperPos_mm.fr));
    radio.write(&pSensorData->damperPos_mm.fl, sizeof(pSensorData->damperPos_mm.fl));
    radio.write(&pSensorData->damperPos_mm.rr, sizeof(pSensorData->damperPos_mm.rr));
    radio.write(&pSensorData->damperPos_mm.rl, sizeof(pSensorData->damperPos_mm.rl));

    radio.write(&pSensorData->gearPos, sizeof(pSensorData->gearPos));

    radio.write(&pSensorData->steeringWheelPos_degrees, sizeof(pSensorData->steeringWheelPos_degrees));

    radio.write(&pSensorData->gyro.x, sizeof(pSensorData->gyro.x));
    radio.write(&pSensorData->gyro.y, sizeof(pSensorData->gyro.y));
    radio.write(&pSensorData->gyro.z, sizeof(pSensorData->gyro.z));

    radio.write(&pSensorData->batteryVoltage_dV, sizeof(pSensorData->batteryVoltage_dV));

    radio.write(&pSensorData->throttlePos_mm, sizeof(pSensorData->throttlePos_mm));

    radio.write(&pSensorData->fuelPressure_pa, sizeof(pSensorData->fuelPressure_pa));

    radio.write(&pSensorData->time_ms, sizeof(pSensorData->time_ms));

    radio.write(&checksum, sizeof(checksum));

    radio.write(&newline, sizeof(newline));

    return true;

}


