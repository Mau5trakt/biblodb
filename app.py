from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


'''
SELECT usuarios.nombres FROM usuarios INNER JOIN prestamo on usuarios.carnet = prestamo.carnet
INNER JOIN libros on prestamo.id_libro = libros.id_libro INNER JOIN isbn_libro on libros.id_libro = isbn_libro.id_libro WHERE isbn_libro.isbn = "9786071505408";


'''
db = SQL("sqlite:///database/biblo.db")

#Registroppp
@app.route("/")
@app.route('/register', methods=["GET","POST"])

def registro():
    session.clear() #Sinceramente no recuerdo
    if request.method == "POST":
        a = db.execute('SELECT * FROM Libros')
        print(a)
        nombres = request.form.get("nombres")
        apellidos = request.form.get("apellidos")
        carrera = request.form.get("carrera")
        print(nombres)
        print(apellidos)
        print(carrera)


    print("a")
    return render_template("prueba-nav.html")
