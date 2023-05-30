#include <Arduino.h>

uint32_t data_output_limit[17][2] = {
    {0, 600},  // Wheel Speed
    {0, 600},  // Wheel Speed
    {0, 600},  // Wheel Speed
    {0, 600},  // Wheel Speed
    {0, 1000}, // Engine Rev
    {0, 100},  // Damper Pos
    {0, 100},  // Damper Pos
    {0, 100},  // Damper Pos
    {0, 100},  // Damper Pos
    {0, 6},    // Gear Pos
    {0, 360},  // Steering Wheel Pos
    {0, 1000}, // Gyro
    {0, 1000}, // Gyro
    {0, 1000}, // Gyro
    {0, 130},  // Battery Voltage
    {0, 100},  // Throttle
    {0, 6000}  // Fuel Pressure
};

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  for (uint32_t i = 0; i <= sizeof(data_output_limit) / sizeof(data_output_limit[0]); i++)
  {
    Serial.print(random(data_output_limit[i][0], data_output_limit[i][1]));
    Serial.print(",");
  }

  Serial.print(millis());
  Serial.println(",CHECK_SUM");
  delay(500);
}
