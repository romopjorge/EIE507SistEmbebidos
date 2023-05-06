#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define DS18B20_PIN 2 // Pin digital donde se conecta el sensor DS18B20
#define SLAVE_ADDRESS 0x08 // Dirección del dispositivo I2C

OneWire oneWire(DS18B20_PIN); //Se establece una instancia OneWire en el pin para comunicarse con el sensor
DallasTemperature sensors(&oneWire); //Se pasa la instancia a la libreria Dallas Temperature

float tempC;

void setup() {
  Wire.begin(SLAVE_ADDRESS); //Se inicializa el bus I2C con el Arduino como esclavo
  Wire.onRequest(requestEvent); //Se identifica la funcion a actuar al existir una solicitud
  sensors.begin(); //Se inicializa el sensor
}

void loop() {
  sensors.requestTemperatures(); //Se solicita la temperatura al sensor
  tempC = sensors.getTempCByIndex(0); //Se guarda el valor en una variable
  delay(1000);
}

void requestEvent() {
  byte* tempCPtr = (byte*)&tempC; //Se pasa el valor de temperatura de float a un array de 4 bytes
  for (int i = 0; i < sizeof(tempC); i++) { //Estructura "for" para pasar por cada posicion del array
    Wire.write(tempCPtr[i]); //Se manda el byte contenido en la posicion "i"
  }
}
