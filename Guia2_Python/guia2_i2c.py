import smbus
import time
import struct

class ArduinoI2C:
    def __init__(self, slave_address):
        self.slave_address = slave_address
        self.bus = smbus.SMBus(1)

    def leer_temperatura(self):
        # Enviar solicitud y leer los 4 bytes de la temperatura enviados por el Arduino
        tempBytes = self.bus.read_i2c_block_data(self.slave_address, 0, 4)

        # Convertir los 4 bytes en un float
        tempC = struct.unpack('<f', bytes(tempBytes))[0]

        # Retornar la temperatura en grados Celsius
        return tempC

if __name__ == '__main__':
    # Dirección del dispositivo I2C
    SLAVE_ADDRESS = 0x08

    # Crear objeto de la clase ArduinoI2C
    arduino = ArduinoI2C(SLAVE_ADDRESS)

    while True:
        # Leer la temperatura actual
        temp_C = arduino.leer_temperatura()

        # Imprimir la temperatura en la consola
        print(f"{temp_C:.2f}")

        # Esperar 30 segundos antes de solicitar la siguiente lectura de temperatura
        time.sleep(30)
