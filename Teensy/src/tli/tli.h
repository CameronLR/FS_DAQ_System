#ifndef RFMODULE_H
#define RFMODULE_H

#include "cmn/daq_common.h"

extern bool rfModule_sendData(sensorData_s *pSensorData);
extern bool rfModule_init();

#endif