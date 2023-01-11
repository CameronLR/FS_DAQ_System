/**
 * @file
 * @brief A file that is documented.
 *
 * Detailed description, etc.
 */

#include <Arduino_LSM6DSOX.h>
#include "gyro.h"

int32_t getGyroX()
{
    return 0;
}

int32_t getGyroY()
{
    return 0;
}

int32_t getGyroZ()
{
    return 0;
}

GyroData_s getGyro()
{
    GyroData_s gyro = {.x = getGyroX(),
                       .y = getGyroY(),
                       .z = getGyroZ()};

    return gyro;
}
