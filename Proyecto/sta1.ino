#include "DHT.h"
#include <ArduinoJson.h>

#define DHTPIN 6
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

char name = 'sta1';

void setup() {
  Serial.begin(9600);

  dht.begin();
}

void loop() {

  if (Serial.available() > 0) {
    char c = Serial.read();
    delay(5);
    if (c == name) {

      StaticJsonDocument<200> json;
      json["id_station"] = 1;

      JsonArray readings = json.createNestedArray("readings");

      JsonObject readings1 = readings.createNestedObject();
      readings1["id"] = 1;
      readings1["reading"] = dht.readTemperature();     

      JsonObject readings2 = readings.createNestedObject();  
      readings2["id"] = 2;
      readings2["reading"] = dht.readHumidity();   

      JsonObject readings3 = readings.createNestedObject();
      readings3["id"] = 3;
      readings3["reading"] = int(25*sqrt(analogRead(0)));      

      serializeJson(json, Serial);
      Serial.println();
    }
  }
}
