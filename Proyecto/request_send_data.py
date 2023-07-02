import serial
import requests

url = "http://ip_maquina_virtual/cgid-bin/first.py"

class Xbee:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(port, 9600)

    def request_data(self, sta):
        self.ser.write(sta)
        data = self.ser.readline().decode().strip()
        return data

coord = Xbee('/dev/ttyUSB0')

sta1 = coord.request_data(b'sta1')
sta2 = coord.request_data(b'sta2')

#print ('Data from Station 1:', sta1)
#print ('Data from Station 2:', sta2)

x = requests.post(url, data = sta1)
x = requests.post(url, data = sta2)
print (x.text)
