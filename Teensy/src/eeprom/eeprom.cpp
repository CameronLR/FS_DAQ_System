/**
 * @file
 * @brief EEPROM handling functions
 *
 * Detailed description, etc.
 */

#include <Arduino.h>
#include <EEPROM.h>

#include <cmn/daq_common.h>
#include "eeprom.h"

typedef enum eepromDataAddr
{
    EEPROM_START_ADDR = 0x00,
    GEAR_POS_ADDR = EEPROM_START_ADDR,
    GEAR_POS_LEN = sizeof(daq_GearPos_t),
    EXAMPLE_NEXT_ADDR = EEPROM_START_ADDR + GEAR_POS_LEN
} eepromDataAddr;

daq_GearPos_t eeprom_readGearPosition()
{
    daq_GearPos_t gearPos = 0U;
    
    EEPROM.get(GEAR_POS_ADDR, gearPos);
    
    return gearPos;
}

void eeprom_writeGearPosition(daq_GearPos_t gearPos)
{
    EEPROM.put(GEAR_POS_ADDR, gearPos);

    return;
}