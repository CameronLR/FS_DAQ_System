#include <Arduino.h>

uint32_t data_output_limit[17] = {
    600,  // Wheel Speed
    600,  // Wheel Speed
    600,  // Wheel Speed
    600,  // Wheel Speed
    1000, // Engine Rev
    100,  // Damper Pos
    100,  // Damper Pos
    100,  // Damper Pos
    100,  // Damper Pos
    6,    // Gear Pos
    360,  // Steering Wheel Pos
    1000, // Gyro
    1000, // Gyro
    1000, // Gyro
    130,  // Battery Voltage
    100,  // Throttle
    6000  // Fuel Pressure
};

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  for (uint32_t i = 0; i <= sizeof(data_output_limit) / sizeof(data_output_limit[0]); i++)
  {
    Serial.print(random(0, data_output_limit[i]));
    Serial.print(",");
  }

  Serial.print(millis());
  Serial.println(",CHECK_SUM");
  delay(500);
}
