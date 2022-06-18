from cs50 import SQL

db = SQL("sqlite:///database/biblo.db")

class Libro():

    def __init__(self, id_libro):
        self.datos = db.execute("SELECT * from libros WHERE id_libro = ?", id_libro)[0]
        return
    def get_titulo(self):
        return self.datos["titulo"]

    def get_clasificacion(self):
        return self.datos["clasificacion"]

    def get_year(self):
        return self.datos["año"]

    def get_edicion(self):
        return self.datos["edicion"]

    def get_autor(self):
        id_libro = self.datos["id_libro"]

        autor = db.execute("SELECT * from libro_autor INNER JOIN autor ON libro_autor.id_autor = autor.id_autor WHERE libro_autor.id_libro = ?", id_libro)
        autor = autor[0]
        return autor
# fecha_de_prestamo	id_libro	carnet	id_trabajador	fecha_de_devolucion	renovaciones	status
def ver_press(carnet, status):
    estudiante = db.execute("SELECT * FROM usuarios WHERE carnet = ?", carnet)[0]

    prestamos_cerrados = db.execute("SELECT * FROM prestamo WHERE carnet = ? AND status = ?", carnet, status)

    encontrados = []

    for prestamo in prestamos_cerrados:

        l = Libro(prestamo["id_libro"])

        respuesta = {
            "nombres": estudiante["nombres"] + " " + estudiante["apellidos"],
            "carnet": carnet,
            "carrera": estudiante["carrera"],
            "id_prestamo": prestamo["id_prestamo"],
            "fecha_prestamo": prestamo["fecha_de_prestamo"],
            "libro": l.get_titulo(),
            "autor":l.get_autor()["nombre"],
            "clasificacion": l.get_clasificacion(),
            "year": l.get_year(),
            "edicion": l.get_edicion()

        }

        encontrados.append(respuesta)


    return encontrados 