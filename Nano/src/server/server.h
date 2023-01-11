#ifndef SERVER_H
#define SERVER_H

#include "../../cmn/daq_common.h"

extern void networkSetup();
extern void uploadDataToServer(sensorData_s *pSensorData);

#endif