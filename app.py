import os
import re
from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for, current_app
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
mail = Mail(app)

Session(app)


'''
SELECT usuarios.nombres FROM usuarios INNER JOIN prestamo on usuarios.carnet = prestamo.carnet
INNER JOIN libros on prestamo.id_libro = libros.id_libro INNER JOIN isbn_libro on libros.id_libro = isbn_libro.id_libro WHERE isbn_libro.isbn = "9786071505408";


'''
db = SQL("sqlite:///database/biblo.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


#Registroppp
@app.route('/register', methods=["GET","POST"])





def registro():
    session.clear() #Sinceramente no recuerdo

    if request.method == "POST":
        #patrones regex para el numero de telefono
        pat_celular = re.compile(r"(((\+[0-9]{1,2}|00[0-9]{1,2})[-\ .]?)?)(\d[-\ .]?){5,15}")
        pat_carnet = re.compile(r"(((\+[0-9]{1,2}|00[0-9]{1,2})[-\ .]?)?)(\d[-\ .]?){5,15}[a-zA*-Z_]")

        carreras = ["Arquitectura", "Ing. Computación", "Ing. Eléctrica", "Ing. Eléctrónica", "Ing. Química" ]


        nombres = request.form.get("nombres")
        apellidos = request.form.get("apellidos")
        carrera = request.form.get("carrera")
        numero = request.form.get("telefono")
        strcarnet = request.form.get("carnet")
        correo = request.form.get("email")
        hash = generate_password_hash(request.form.get("pass"))

        if carrera not in carreras:
            return apology("Esa no es una carrera", 400)

        if re.fullmatch(pat_celular, numero):
            caracteres = "+- "
            for a in range(len(caracteres)):
                numero = numero.replace(caracteres[a], "")
        else:
            return apology("Ingrese un numero de celular valido",403)

        celular = int(numero)

        if re.fullmatch(pat_carnet, strcarnet):
            strcarnet = re.sub("\+|\ '|\-|[a-zA-Z_]","",strcarnet)
            carnet = int(strcarnet)
            print("********")
            print(carnet)
        else:
            return apology("Ingrese un numero de carnet válido", 400)




        app.logger.info(carnet)


        #verificar si el usuario existe en la base de datos
        if len(db.execute("SELECT carnet from usuarios where carnet = ?", carnet)) != 0:
            return(apology("Este carnet ya se encuentra registrado"))

            #Puedo probar a poner un flash diciendole que ya tiene cuenta
            #y redireccionarlo a la funcion iniciar sesion

        else:
        #Ingresando datos a la database
            db.execute("INSERT INTO usuarios(carnet, nombres, apellidos, email, hash, carrera, telefono) VALUES(?,?,?,?,?,?,?)", carnet, nombres, apellidos, correo, hash, carrera, celular)
            msg = Message("Registro Exitoso", recipients=[correo])
            msg.html =f""" <h1> Hola {nombres} {apellidos}, bienvenido a Biblodb </h1>
                            <p> Te has registrado exitosamente en la biblioteca </p>
                            <p> mensaje generado automáticamente el: {datetime.now()} </p>
                        """
            mail = Mail(current_app)
            mail.send(msg)

        return redirect(url_for('inicio'))


    return render_template("index.html")



@app.route('/iniciar', methods=["GET", "POST"])
def inicio():
    session.clear()
    pat_carnet = re.compile(r"(((\+[0-9]{1,2}|00[0-9]{1,2})[-\ .]?)?)(\d[-\ .]?){5,15}[a-zA*-Z_]")
    if request.method == "POST":

        if not request.form.get("carnet"):
            return apology("Ingrese su carné", 403)

        if not request.form.get("password"):
            return apology("Ingrese su contraseña", 403)


        strcarnet = request.form.get("carnet")

        if re.fullmatch(pat_carnet, strcarnet):
            strcarnet = re.sub("\+|\ '|\-|[a-zA-Z_]","",strcarnet)
            carnet = int(strcarnet)
            print("********")
            print(carnet)
        else:
            return apology("Ingrese un numero de carnet válido", 403)


        #pasw = generate_password_hash(request.form.get("password"))
        usuario = db.execute("SELECT * FROM usuarios WHERE carnet = ?", carnet)

        if len(usuario) != 1 or not check_password_hash(usuario[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["carnet"] = usuario[0]["carnet"]


        return redirect("/")


    return render_template('isesion.html')



@app.route('/', methods=["GET", "POST"])
@login_required
def usuariohome():
    print("Only for the pr")

    return render_template("ulogin.html")
