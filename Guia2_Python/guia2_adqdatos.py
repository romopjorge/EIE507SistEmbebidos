import smbus
import time
import struct
from datetime import datetime

class ArduinoI2C:

    def __init__(self, slave_address):
        self.slave_address = slave_address
        self.bus = smbus.SMBus(1)

    def leer_temperatura(self):
        # Enviar solicitud y leer los 4 bytes de la temperatura enviados por el Arduino
        tempBytes = self.bus.read_i2c_block_data(self.slave_address, 0, 4)

        # Convertir los 4 bytes en un float
        tempC = struct.unpack('<f', bytes(tempBytes))[0]

        # Devolver la temperatura
        return tempC

class DataLogger:
    def __init__(self,esclavo, archivo, cant_datos):
        self.esclavo = esclavo
        self.archivo = archivo
        self.cant_datos = cant_datos
        self.datos = []

    def loop(self):
        while True:
            # Leer la temperatura y el timestamp
            temp_C = self.esclavo.leer_temperatura()

            # Se obtiene la fecha actual
            timestamp = datetime.now()

            # Se imprime la fecha actual y la temperatura
            print(f"{timestamp}: {temp_C:.2f}°C")

            # Agregar el valor de la temperatura a la lista de muestras
            self.datos.append(temp_C)

            # Si se han tomado suficientes muestras, calcular el promedio y escribirlo en el archivo de log
            if len(self.datos) == self.cant_datos:

                # Se obtiene la hora y fecha actual
                timestamp = datetime.now()

                # Calculo del promedio
                prom_temp = sum(self.datos) / len(self.datos)

                # Se imprime la fecha actual y el promedio de temperatura
                print(f'{timestamp}: {prom_temp:.2f}°C\n')

                # Escribir el promedio de las muestras y el timestamp en el archivo de log
                with open(self.archivo, 'a') as f:
                    f.write(f'{timestamp}: {prom_temp:.2f}\n')

                # Limpiar la lista de muestras
                self.datos.clear()

            # Esperar el intervalo de tiempo especificado antes de tomar la siguiente muestra
            time.sleep(30)

if __name__ == '__main__':
    # Dirección del dispositivo I2C
    SLAVE_ADDRESS = 0x08

    # Crear objeto de la clase ArduinoI2C
    arduino = ArduinoI2C(SLAVE_ADDRESS)

    # Crear objeto de la clase DataLogger(10 muestras x 30 segundos = 5 minutos)
    datalogger = DataLogger(arduino,'temp_log.txt',10)

    # Se ejecuta el loop de datalogger
    datalogger.loop()
