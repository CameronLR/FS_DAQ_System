/**
 * @file
 * @brief EEPROM handling functions
 *
 * Detailed description, etc.
 */

#include <Arduino.h>
#include <EEPROM.h>

typedef enum eepromDataAddr
{
    EEPROM_START_ADDR = 0x00,
    GEAR_POS_ADDR = EEPROM_START_ADDR,
    GEAR_POS_LEN = 0x04,
    EXAMPLE_NEXT_ADDR = EEPROM_START_ADDR + GEAR_POS_LEN
} eepromDataAddr;

uint32_t eeprom_readGearPosition()
{
    uint32_t gearPos = 0U;
    
    EEPROM.get(GEAR_POS_ADDR, gearPos);
    
    return gearPos;
}

void eeprom_writeGearPosition(uint32_t gearPos)
{
    EEPROM.put(GEAR_POS_ADDR, gearPos);

    return;
}