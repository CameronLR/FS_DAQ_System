#include <Arduino.h>

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  for (int i = 0; i < 4; i++)
  {
    Serial.print(random(0, 1000));
    Serial.print(",");
  }
  Serial.println("CHECK_SUM");
  delay(500);
}