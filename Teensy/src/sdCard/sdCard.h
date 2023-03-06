#ifndef SDCARD_H
#define SDCARD_H

#include "../../cmn/daq_common.h"

extern bool sendDataToSdCard(sensorData_s *pSensorData);
extern bool sdCard_init();


#endif