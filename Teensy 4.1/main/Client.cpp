// Utsav (MJ)'s Code - from a past project and not utilising our boards

#include <WiFi.h>
#include <HTTPClient.h>
#include "Arduino.h'

#define print(string) Serial.print(string);

//network details
const char* ssid = "WIFI-NETWORK NAME";
const char* password = "password";

String serverName = "http://192.168.0.120:8080/Server.php"; // Location to send POSTed data

String apiKeyValue = "tPmAT5Ab3j7F9";

String deviceName = "ESP32"; //model


void setup() 
{
 Serial.begin(115200);
 
 //connect to the wireless network
 WiFi.begin(ssid, password);
 print("Connecting");
 
 while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    print(".");
    }

 print("\n");
 print("\nConnected to WiFi network with IP Address: ");
 print(WiFi.localIP());
 
}

//function accepts a location value and sends that to the server.
void sendData(String loc)
{
    if(WiFi.status()== WL_CONNECTED)
    {
        HTTPClient http;
        // Prepare your HTTP POST request data
        String httpRequestData = "api_key=" + apiKeyValue + "&value1=" + deviceName + "&value2="+ loc + "";
        print("\n httpRequestData: ");
        print(httpRequestData);

        // Your Domain name with URL path or IP address with path
        String serverPath = serverName +"?"+httpRequestData;
        http.begin(serverPath.c_str());

        // Send HTTP GET request
        int httpResponseCode = http.GET();

        if (httpResponseCode>0) 
        {
            print("\nHTTP Response code: ");
            print(httpResponseCode);
        }
        else 
        {
            print("\nError code: ");
            print(httpResponseCode);
        }
        // Free resources
        http.end();
    }
    else 
    {
        print("\nWiFi Disconnected");
    }
}

