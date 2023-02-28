#ifndef EEPROM_H
#define EEPROM_H

#include <stdint.h>

extern uint32_t eeprom_readGearPosition();
extern void eeprom_writeGearPosition(uint32_t gearPos);

#endif