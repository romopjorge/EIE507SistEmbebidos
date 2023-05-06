import smbus
import time
import struct

# Dirección del dispositivo I2C
SLAVE_ADDRESS = 0x08

# Inicializar el bus I2C
bus = smbus.SMBus(1)

while True:

    # Enviar solicitud y leer los 4 bytes de la temperatura enviados por el Arduino
    tempBytes = bus.read_i2c_block_data( 8, 0, 4)

    # Convertir los 4 bytes en un float
    tempC = struct.unpack('<f', bytes(tempBytes))[0]

    # Imprimir la temperatura en la consola
    print(f"{tempC}")

    # Esperar 30 segundos antes de solicitar la siguiente lectura de temperatura
    time.sleep(30)
