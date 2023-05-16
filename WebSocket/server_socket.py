#Importación librerias
import socket
import threading

#Definición de las variables globales
HEADER = 64
PORT = 3080
SERVER = '192.168.1.81'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
VALIDATION = False        #Bandera (utilizada en la validación de la MAC)
MAC_SERVER = '3C:95:09:B2:02:BC'        #MAC almacenada en el servidor de la MAC del cliente
KEY = 10                  #KEY utilizada para desencriptar el mensaje

#Se asocia el socket del servidor a un puerto especifico
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def validation_mac(mac_client, mac_server):
  if mac_client == mac_server:
    msg = "MAC VALIDADA"
    return True, msg
  else:
    msg = "MAC INCORRECTA"
    return False, msg

def decrypt_message(msg):
  decrypted_data = ""
  for char in msg:
      decrypted_char = chr(ord(char) - KEY)
      decrypted_data += decrypted_char
  return decrypted_data

def handle_client(conn, addr):
  print(f"[NEW CONNECTION] {addr} connected.")
  connected = True

  #Mientras se mantenga la conexión
  while connected:
      msg_length = conn.recv(HEADER).decode(FORMAT)

      #Se valida el tamaño del mensaje
      if msg_length:
          msg_length = int(msg_length)
          msg = conn.recv(msg_length).decode(FORMAT)
          decrypted_message = decrypt_message(msg)

          #Se valida que el mensaje de desconexión
          if decrypted_message == DISCONNECT_MESSAGE:
              connected = False

          global VALIDATION
          #Se valida la MAC recibida
          if not VALIDATION:
              VALIDATION, msg = validation_mac(decrypted_message, MAC_SERVER)
              print(msg)
              conn.send(msg.encode(FORMAT))
          else:
            print(f"[{addr}] {decrypted_message}")
            conn.send("Msg received".encode(FORMAT))

  conn.close()

def start():
    server.listen()
    print(f"[LISTEN] Server is listening on address {ADDR}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

#Se levanta el servidor
print("[STARTING] server is running.....")
start()
