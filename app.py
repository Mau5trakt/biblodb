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
@app.route("/index")
@app.route('/register', methods=["GET","POST"])

def registro():
    session.clear() #Sinceramente no recuerdo

    if request.method == "POST":
        carreras = ["Arquitectura", "Ing. Computación", "Ing. Eléctrica", "Ing. Eléctrónica", "Ing. Química" ]
        a = db.execute('SELECT * FROM Libros')
        print(a)
        nombres = request.form.get("nombres")
        apellidos = request.form.get("apellidos")
        carrera = request.form.get("carrera")
        numero = request.form.get("telefono") # Verificar lo del numero de telefono con el regex
        strcarnet = request.form.get("carnet")
        correo = request.form.get("email")
        hash = generate_password_hash(request.form.get("pass"))

        if carrera not in carreras:
            return apology("Esa no es una carrera", 400)
        try:
            carnet = int(strcarnet)
            celular = int(numero)
        except ValueError:
            return apology("Ingrese solo numeros")

        #Ingresando datos a la database
        db.execute("INSERT INTO usuarios(carnet, nombres, apellidos, email, hash, carrera, telefono) VALUES(?,?,?,?,?,?,?)", carnet, nombres, apellidos, correo, hash, carrera, celular)

        return redirect(url_for('inicio'))


    return render_template("index.html")



@app.route('/iniciar', methods=["GET", "POST"])
def inicio():
    session.clear()
    if request.method == "POST":

        if not request.form.get("carnet"):
            return apology("Ingrese su carné", 403)

        if not request.form.get("password"):
            return apology("Ingrese su contraseña", 403)


        strcarnet = request.form.get("carnet")
        try:
            intcarnet = int(strcarnet)
        except ValueError:
            return apology("Ingrese solo numeros")

        #pasw = generate_password_hash(request.form.get("password"))
        usuario = db.execute("SELECT * FROM usuarios WHERE carnet = ?", intcarnet)

        if len(usuario) != 1 or not check_password_hash(usuario[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["carnet"] = usuario[0]["carnet"]

        return redirect(url_for('usuariohome'))

    return render_template('isesion.html')



@app.route('/homepage', methods=["GET", "POST"])
def usuariohome():

    return render_template("ulogin.html")
