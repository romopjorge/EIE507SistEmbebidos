import serial

class LecturaSerial:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.reset_input_buffer()

    def leer_linea(self):
        if self.ser.in_waiting > 0:
            linea = self.ser.readline().decode('utf-8').rstrip()
            return linea
        else:
            return None

lectura = LecturaSerial()
while True:
    linea = lectura.leer_linea()
    if linea is not None:
        print(linea)
