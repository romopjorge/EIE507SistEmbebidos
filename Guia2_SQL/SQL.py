import psycopg2

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
        print("Conectado a la base de datos")

    def consultar(self, sql):
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        return resultado

    def ejecutar(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()
        print("Operación realizada correctamente")

    def cerrar(self):
        self.cursor.close()
        self.connection.close()
        print("Conexion terminada")

db = Database("localhost", "5432", "postgres", "Admin.123", "postgres")
db.conectar()
# Ejemplo comando SQL via Python
resultado = db.consultar("SELECT first_name, email FROM staff")
# Primer Ejemplo INNER JOIN
#resultado = db.consultar("""
#SELECT actor.first_name, film.title
#FROM actor
#JOIN film_actor
#ON actor.actor_id = film_actor.actor_id
#JOIN film
#ON film_actor.film_id = film.film_id""")
# Segundo Ejemplo INNER JOIN
#resultado = db.consultar("""
#SELECT film.title, category.name
#FROM film
#JOIN film_category
#ON film.film_id = film_category.film_id
#JOIN category
#ON film_category.category_id = category.category_id""")
# Tercer Ejemplo INNER JOIN
#resultado = db.consultar("""
#SELECT staff.first_name, country.country
#FROM staff
#JOIN address
#ON staff.address_id = address.address_id
#JOIN city
#ON address.city_id = city.city_id
#JOIN country
#ON city.country_id = country.country_id""")
print(resultado)
db.cerrar()
