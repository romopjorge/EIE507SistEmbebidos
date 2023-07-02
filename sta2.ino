#include <Adafruit_BMP085.h>
#include "DHT.h"
#include <ArduinoJson.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

Adafruit_BMP085 bmp;

char name = 'sta2';
  
void setup() {
  Serial.begin(9600);

  bmp.begin();

  dht.begin();

  pinMode(7, OUTPUT);
	digitalWrite(7, LOW);
}
  
void loop() {

    if (Serial.available() > 0) {
    char c = Serial.read();
    delay(5);
    if (c == name) {

      StaticJsonDocument<200> json;
      json["id_station"] = 2;

      JsonArray readings = json.createNestedArray("readings");

      JsonObject readings1 = readings.createNestedObject();
      readings1["id"] = 1;
      readings1["reading"] = dht.readTemperature();     

      JsonObject readings2 = readings.createNestedObject();  
      readings2["id"] = 2;
      readings2["reading"] = dht.readHumidity();   

      JsonObject readings3 = readings.createNestedObject();
      readings3["id"] = 4;
      readings3["reading"] = bmp.readPressure();   

      JsonObject readings4 = readings.createNestedObject();
      readings4["id"] = 5;
      readings4["reading"] = int(bmp.readAltitude(101900));

      digitalWrite(7, HIGH);

      JsonObject readings5 = readings.createNestedObject();
      readings5["id"] = 6;
      readings5["reading"] = map(analogRead(0),0,1024,0,400);   

      digitalWrite(7, LOW);

      serializeJson(json, Serial);
      Serial.println();

    }
  }
}
