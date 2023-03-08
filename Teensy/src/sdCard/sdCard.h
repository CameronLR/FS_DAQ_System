#ifndef SDCARD_H
#define SDCARD_H

#include "../../cmn/daq_common.h"

extern bool sdCard_appendLine(sensorData_s *pSensorData);
extern bool sdCard_init();


#endif