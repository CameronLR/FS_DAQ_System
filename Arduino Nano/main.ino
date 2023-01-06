void setup(){


}

void loop(){
    // sends gyro data to Teensy 4.1
    SendGyro();
    // retrieves all the data from the Teensy 4.1
    RetrieveAllData();
    // uploads all data to database 
    UploadToDataBase();
}
