#include <OneWire.h>
#include <DallasTemperature.h>

#define DS18B20_PIN 2 // Pin digital donde se conecta el sensor DS18B20

OneWire oneWire(DS18B20_PIN); //Se establece una instancia OneWire en el pin para comunicarse con el sensor
DallasTemperature sensors(&oneWire); //Se pasa la instancia a la libreria Dallas Temperature

float ultmedicion = 0;

void setup() {
  Serial.begin(9600); //Se inicializa el puerto serial
  sensors.begin(); //Se inicializa el sensor
}

void loop() {
  if (millis() - ultmedicion >= 5000){ //Se envía valor de temperatura cada 5 segundos
    ultmedicion = millis(); //Se guarda el momento en que se envió el ultimo dato
    sensors.requestTemperatures(); //Se solicita la temperatura al sensor
    Serial.println(sensors.getTempCByIndex(0)); //Se imprime en el puerto serial el valor sensado
  }
}
