#Importación de la libreria socket y uuid (para obtener la mac del cliente)
import socket
from uuid import getnode as get_mac

#Definición de las variables globales
HEADER = 64
PORT = 3080
SERVER = '192.168.1.81'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
KEY = 10                  #KEY utilizada para encriptar el mensaje

#Definición del cliente y conexión del mismo
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def encrypt_message(msg):
  encrypted_data = ""

  for char in str(msg):
        encrypted_char = chr(ord(char) + KEY)
        encrypted_data += encrypted_char

  return encrypted_data


def get_mac_client():
  mac = '%012X' % get_mac()
  mac_client = ':'.join(mac[i:i+2] for i in range(0, len(mac), 2)) 

  #Se da formato legible a la MAC
  return mac_client


def send(msg):
    encrypted_msg = encrypt_message(msg)
    message = encrypted_msg.encode(FORMAT)

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    send_length += b' '*(HEADER-len(send_length))

    client.send(send_length)
    client.send(message)

    print(client.recv(2048).decode(FORMAT))

# Se envía la MAC para validarla en el servidor
mac_client = get_mac_client()
send(mac_client)
input()
# Se envían los mensajes una vez válidada la MAC
send('hello')
input()
send('asdfasdf')
input()
send(DISCONNECT_MESSAGE)