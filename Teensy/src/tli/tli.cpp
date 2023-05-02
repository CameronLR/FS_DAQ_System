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
#include "tli.h"

#include "RF24.h"
#include "nRF24L01.h" 

#define CE_PIN 9 //Theese can be any
#define CSN_PIN 10 
#define TX_BUFFER_SIZE 150

// MOSI: - pin 11 
// MISO: - pin 12
// SCK: - pin 13

RF24 radio(CE_PIN, CSN_PIN);
const byte address[6] = "00001";
const byte checksum = 0;

char pTxBuffer [TX_BUFFER_SIZE];

bool tli_init() 
{

    if (!radio.begin()) {
        //may need to wait here
        Serial.println("ERROR: Unable to connect to rfModule");
        return false;
    }

    radio.setDataRate(RF24_250KBPS);           // greater = more distance
    radio.setPALevel(RF24_PA_MAX);             // alternative is RF24_PA_LOW.
    
    radio.setPayloadSize(32);                  //32 byte packtes (default and largest possible)
    radio.openWritingPipe(address);            //Set to TX
    radio.stopListening();

    return true;
}


bool tli_sendData(sensorData_s *pSensorData)
{

    int32_t txBufferSize = snprintf ( pTxBuffer, TX_BUFFER_SIZE, "%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%d\n", 
    pSensorData->wheelSpeed_mph.fr, 
    pSensorData->wheelSpeed_mph.rr, 
    pSensorData->wheelSpeed_mph.fl, 
    pSensorData->wheelSpeed_mph.rl, 
    pSensorData->engineRev_rpm, 
    pSensorData->damperPos_mm.fr, 
    pSensorData->damperPos_mm.fl, 
    pSensorData->damperPos_mm.rr, 
    pSensorData->damperPos_mm.rl, 
    pSensorData->gearPos, 
    pSensorData->steeringWheelPos_degrees, 
    pSensorData->gyro.x, 
    pSensorData->gyro.y, 
    pSensorData->gyro.z, 
    pSensorData->batteryVoltage_dV, 
    pSensorData->throttlePos_mm, 
    pSensorData->fuelPressure_pa, 
    checksum);

    //Send i whole 32 byte chunks using the usedBufferSpace too calc i (could be a while loop)
    int32_t i;


    for (i = 0; i < (floor(txBufferSize / 32)); i++ ){
        radio.write(pTxBuffer + (32 * i), 32); 
    }
    
    //Send anything remaining after the 32 byte chunks
    radio.write(pTxBuffer + ((i + 1) * 32), txBufferSize % 32);

    return true;
} 
