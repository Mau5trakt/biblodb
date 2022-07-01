from cs50 import SQL
from datetime import timedelta, datetime, date
import re

db = SQL("sqlite:///database/respaldo.db")

pat_numerico = re.compile(r"(\d+)((\d+)+)?")

class Libro():

    def __init__(self, id_libro):
        self.datos = db.execute("SELECT * from libros WHERE id_libro = ?", id_libro)[0]
        return

    def get_id_libro(self):
        return self.datos["id_libro"]

    def get_isbn(self):
        return self.datos["isbn"]

    def get_titulo(self):
        return self.datos["titulo"]

    def get_autor(self):
        return self.datos["autor"]

    def get_year(self):
        return self.datos["year"]

    def get_clasificacion(self):
        return self.datos["clasificacion"]

    def get_descriptor(self):
        return self.datos["descriptor"]

    def get_edicion(self):
        return self.datos["edicion"]

    def get_imagen(self):
        return self.datos["imagen"]

    def get_editorial(self):
        return self.datos["editorial"]

def ver_press(carnet, status):
    estudiante = db.execute("SELECT * FROM usuarios WHERE carnet = ?", carnet)[0]

    prestamos_cerrados = db.execute("SELECT * FROM prestamo WHERE prestamo.u_carnet = ? AND status = ?", carnet, status)

    encontrados = []

    for prestamo in prestamos_cerrados:

        l = Libro(prestamo["libro_id"])

        respuesta = {
            "nombres": estudiante["nombres"] + " " + estudiante["apellidos"],
            "carnet": carnet,
            "carrera": estudiante["carrera"],
            "id_prestamo": prestamo["id_prestamo"],
            "id_libro": prestamo["libro_id"],
            "titulo": l.get_titulo(),
            "autor": l.get_autor(),
            "year": l.get_year(),
            "clasificacion": l.get_clasificacion(),
            "descriptor": l.get_descriptor(),
            "edicion": l.get_edicion(),
            "imagen": l.get_imagen(),
            "editorial": l.get_editorial(),
            "fecha_prestamo": prestamo["fecha_prestamo"]
        }

        encontrados.append(respuesta)

    return encontrados

def unicarreras():
    carreras = ["Arquitectura", "Ing. Agronoma", "Ing. Civil", "Ing. Computación", "Ing. Eléctrica",
                "Ing. Eléctrónica","Ing. Industrial", "Ing. Química", "Ing. Sistemas", "Ing. Telecomunicaciones", "Otra"]

    return carreras

def buscar_libro(q):

    texto = """ SELECT id_libro, isbn,titulo, autor, year,descriptor, count(libros.titulo) as disponibles FROM inventario INNER JOIN libros
            ON inventario.libro_id = libros.id_libro
            WHERE estado = 0
            AND (libros.titulo LIKE ?
            OR libros.autor LIKE ?
            OR libros.descriptor LIKE ?)

            GROUP BY libros.id_libro"""
    q = "%" + q + "%"

    consulta = db.execute(texto,q,q,q)
    # MOSTRAR SOLO LOS QUE NO ESTAN PRESTADOS
    encontrados = []

    for libro in consulta:

        l = Libro(libro["id_libro"])

        respuesta = {
            "id_libro": libro["id_libro"],
            "isbn": libro["isbn"],
            "titulo": libro["titulo"],
            "autor": l.get_autor(),
            "year": l.get_year(),
            "clasificacion": l.get_clasificacion(),
            "descriptor": l.get_descriptor(),
            "edicion": l.get_edicion(),
            "imagen": l.get_imagen(),
            "editorial": l.get_editorial()
        }

        encontrados.append(respuesta)

    return encontrados

#Verificadores

def verificar_disponibles(isbn):
    cantidad = db.execute("SELECT COUNT(*) from libros INNER JOIN inventario on (libros.id_libro = inventario.libro_id) WHERE libros.isbn = ? AND inventario.estado = 0", isbn)[0]["COUNT(*)"]
    if cantidad >= 3:
        return True
    else:
        return False

def verificar_fechas(fecha):

    hoy = datetime.strptime(str(date.today()), "%Y-%m-%d")
    fecha = datetime.strptime(fecha, "%Y-%m-%d")
    diferencia = fecha - hoy
    if diferencia.days < 0:
        return False #Verificador da falso
    else:
        return True


def verificar_vencido(carnet):
    prestamos = db.execute("SELECT fecha_devolucion, renovaciones FROM prestamo WHERE prestamo.u_carnet = ? AND status = 1", carnet)

    verificadores = []

    for prestamo in prestamos:
         a = verificar_fechas(prestamo["fecha_devolucion"])
         verificadores.append(a)

    #print(verificadores)

    if len(verificadores) == 0 or False not in verificadores:
        return True
    else:
        return False


def verificar_enprestamo(carnet):
    cantidad = db.execute("SELECT COUNT(*) from prestamo WHERE prestamo.u_carnet = ? AND status = 1 or status = 2", carnet)[0]["COUNT(*)"]
    if cantidad < 2 :
        return True
    else:
        return False

def verificar_nolotenga(carnet, isbn):
    cantidad = db.execute("SELECT COUNT(*) from prestamo INNER JOIN libros ON(prestamo.libro_id = libros.id_libro) WHERE u_carnet = ? and isbn = ? and status = 1", carnet, isbn)[0]["COUNT(*)"]
    if cantidad == 0:
        return True
    else:
        return False

def verificar_entramite(carnet, isbn): #Verificar que no tenga en tramite el mismo libro varias veces
    cantidad = db.execute("SELECT COUNT(*) from prestamo INNER JOIN libros l on l.id_libro = prestamo.libro_id where u_carnet = ? and status = 2 and isbn = ?",carnet,isbn)[0]["COUNT(*)"]
    if cantidad == 0:
        return True
    else:
        return False


def fecha_prestamo():
    hoy = date.today()
    agg = timedelta(days=7)
    fecha_prestamo = hoy + agg
    return str(fecha_prestamo)

def tramites():
    entramite = []
    consulta = db.execute("SELECT * FROM prestamo INNER JOIN libros l on l.id_libro = prestamo.libro_id where status = 2")
    for libro in consulta:

        l = Libro(libro["id_libro"])

        respuesta = {
            "id_libro": libro["id_libro"],
            "id_prestamo": libro["id_prestamo"],
            "usuario": libro["u_carnet"],
            "isbn": libro["isbn"],
            "titulo": libro["titulo"],
            "autor": l.get_autor(),
            "year": l.get_year(),
            "clasificacion": l.get_clasificacion(),
            "descriptor": l.get_descriptor(),
            "edicion": l.get_edicion(),
            "imagen": l.get_imagen(),
            "editorial": l.get_editorial()
        }

        entramite.append(respuesta)


    return entramite

def confirmar_numerico(cantidad):
    if re.fullmatch(pat_numerico, cantidad):
        qty = int(cantidad)
        return qty
    else:
        return False


def agregar_libros(cantidad, isbn, titulo, autor, year, clasificacion, descriptor, edicion, imagen, editorial):
    for a in range(cantidad):
        db.execute("INSERT INTO libros (isbn, titulo, autor, year, clasificacion, descriptor, edicion, imagen, editorial) VALUES (?,?,?,?,?,?,?,?,?)", isbn,titulo,autor,year,clasificacion,descriptor, edicion,imagen, editorial)
        inventario_id = db.execute("SELECT COUNT(libros.id_libro) FROM libros")[0]["COUNT(libros.id_libro)"]
        db.execute("INSERT INTO inventario (libro_id, fecha_ingreso) VALUES (?,?)", inventario_id, date.today())

def contar_libros(isbn):
    cantidad = db.execute("SELECT COUNT(*) FROM libros INNER JOIN inventario on (libros.id_libro = inventario.libro_id) WHERE isbn = ? AND estado = 0", isbn)[0]["COUNT(*)"]
    if cantidad != 0:
        return True
    else:
        return False

def verificar_tramitesala(carnet, isbn): #Verificar que no tenga en tramite el mismo libro varias veces
    cantidad = db.execute("SELECT COUNT(*) from prestamo INNER JOIN libros l on l.id_libro = prestamo.libro_id where u_carnet = ? and status = 4 and isbn = ?",carnet,isbn)[0]["COUNT(*)"]
    if cantidad == 0:
        return True
    else:
        return False


