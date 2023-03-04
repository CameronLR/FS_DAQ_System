#ifndef EEPROM_H
#define EEPROM_H

#include <cmn/daq_common.h>

extern daq_GearPos_t eeprom_readGearPosition();
extern void eeprom_writeGearPosition(daq_GearPos_t gearPos);

#endif