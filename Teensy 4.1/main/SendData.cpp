#include "main.h"
#include "Arduino.h"

void SendData(){
    UploadToEEProm();
    UploadToSDCard();
    UploadToDataBase();
}

UploadToEEProm(){
    // code to non-destructively send the data to the EEProm

}

UploadToSDCard(){
    // code to non-destructively send the data to the SD card

}

UploadToDataBase(){ 
    // code to non-destructively send the data to the DataBase
    // this will first have to send the data to the Nano via the serial TX/RX 
    // this is because only the Nano has WiFi capabilities
    // RTC time should also be sent to the database 
     
}