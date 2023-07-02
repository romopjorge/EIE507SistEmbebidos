#!/usr/bin/env python3
import psycopg2
import os
import sys
import json

from datetime import datetime, timedelta, timezone

class Database:

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def conectar(self):
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def ejecutar(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def cerrar(self):
        self.cursor.close()
        self.connection.close()

datalength = int(os.environ["CONTENT_LENGTH"])

rawdata = sys.stdin.read(datalength)
data = eval(rawdata)
timestamp = datetime.now(tz=timezone(timedelta(hours=-4)))

db = Database("localhost", "5432", "postgres", "1234", "postgres")
db.conectar()

for i in data["readings"]:
	idsta = data["id_station"]
	idcat = i["id"]
	value = i["reading"]
	db.ejecutar("INSERT INTO readings(id_station, id_category, value, timestamp) values ( %s, %s, %s, '%s');" % (idsta,idcat,value,timestamp))

db.cerrar

print ("Content-Type: text/html")
print ()
print ("<html>")
print ("<head>")
print ("<title>Respuesta</title>")
print ("</head>")
print ("<body>")
print ("<h1>Datos almacenados correctamente</h1>")
print ("</body>")
print ("</html>")
