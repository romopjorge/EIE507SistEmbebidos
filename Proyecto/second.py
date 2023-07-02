#!/usr/bin/env python3
import psycopg2
import os
import cgi
import cgitb
import pandas as pd

cgitb.enable()

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

    def consultar(self, sql):
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

    def cerrar(self):
        self.cursor.close()
        self.connection.close()

form = cgi.FieldStorage()

sta = form.getvalue("sta")
cat = form.getvalue("cat")

db = Database("localhost", "5432", "postgres", "1234", "postgres")
db.conectar()
if cat == "0":
    resultado = db.consultar("SELECT category.name_category, readings.value, category.symbol, readings.timestamp FROM readings JOIN category ON readings.id_category = category.id_category WHERE (readings.id_station = %s) ORDER BY readings.id_reading DESC;" % sta)
else:
    resultado = db.consultar("SELECT category.name_category, readings.value, category.symbol, readings.timestamp FROM readings JOIN category ON readings.id_category = category.id_category WHERE (readings.id_station = %s AND readings.id_category = %s) ORDER BY readings.id_reading DESC;" % (sta, cat))
df = pd.DataFrame()
for x in resultado:
    df2 = pd.DataFrame(list(x)).T
    df = pd.concat([df, df2])
db.cerrar()

print ("Content-Type: text/html")
print ()
print ("<html>")
print ("<head>")
print ("<title>Respuesta</title>")
print ("</head>")
print ("<body>")
print ("<h1>Datos cargados correctamente (Estacion %s) </h1>" % sta)
print ("</body>")
print ("</html>")
print (df.to_html())
