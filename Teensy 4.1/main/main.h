// Main functions

int GetWheelSpeed();
int GetEngineRevs();
int GetDamperPosition();
int GetGearPosition();
int GetSteeringWheelPosition();
int GetStrain();
int GetGyroX(); // Gyro info will have to be retrieved from Arduino Nano
int GetGyroY(); // Alternatively a seperate gyro could be purchased
int GetGyroZ();
int GetVBat();
int GetThrottlePosition();
int GetFuelPressure();
void SendData();