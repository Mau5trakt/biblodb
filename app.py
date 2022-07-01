import os
import re
from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for, current_app, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, admin_required
from flask_mail import Mail, Message
from functions import *
from datetime import timedelta, date

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

db = SQL("sqlite:///database/respaldo.db")

#patrones regex para el numero de telefono y carnet
pat_celular = re.compile(r"(((\+[0-9]{1,2}|00[0-9]{1,2})[-\ .]?)?)(\d[-\ .]?){5,15}")
pat_carnet = re.compile(r"(((\+[0-9]{1,2}|00[0-9]{1,2})[-\ .]?)?)(\d[-\ .]?){5,15}[a-zA*-Z_]")




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
    session.clear()

    if request.method == "POST":
        carreras = unicarreras()
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
        else:
            return apology("Ingrese un numero de carnet válido", 400)




        #app.logger.info(carnet)


        #verificar si el usuario existe en la base de datos
        if len(db.execute("SELECT carnet from usuarios where carnet = ?", carnet)) != 0:
            return(apology("Este carnet ya se encuentra registrado"))

            #Puedo probar a poner un flash diciendole que ya tiene cuenta
            #y redireccionarlo a la funcion iniciar sesion

        else:
        #Ingresando datos a la database
            try:
                db.execute("INSERT INTO usuarios(carnet, nombres, apellidos, email, hash, carrera, telefono) VALUES(?,?,?,?,?,?,?)", carnet, nombres, apellidos, correo, hash, carrera, celular)
                msg = Message("Registro Exitoso", recipients=[correo])
                msg.html =f""" <h1> Hola {nombres} {apellidos}, bienvenido a Biblodb </h1>
                            <p> Te has registrado exitosamente en la biblioteca </p>
                            <p> mensaje generado automáticamente el: {datetime.now()} </p>
                        """
                mail = Mail(current_app)
                mail.send(msg)

                return redirect(url_for('inicio'))

            except:
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

        if re.fullmatch(pat_carnet, strcarnet):
            strcarnet = re.sub("\+|\ '|\-|[a-zA-Z_]","",strcarnet)
            carnet = int(strcarnet)
        else:
            return apology("Ingrese un numero de carnet válido", 403)


        #pasw = generate_password_hash(request.form.get("password"))
        if strcarnet[:4] == "9999":
            trabajador = db.execute("SELECT * FROM trabajadores WHERE id_trabajador = ?", carnet)
            session["id_trabajador"] = trabajador[0]["id_trabajador"]
            return redirect (url_for('admin'))
        else:
            usuario = db.execute("SELECT * FROM usuarios WHERE carnet = ?", carnet)

        if len(usuario) != 1 or not check_password_hash(usuario[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["carnet"] = usuario[0]["carnet"]




        return redirect("/")


    return render_template('isesion.html')



@app.route('/', methods=["GET", "POST"])
@login_required
def usuariohome():
    carnet = session["carnet"]
    activos = db.execute("SELECT * FROM prestamo INNER JOIN libros on (prestamo.libro_id = libros.id_libro) where u_carnet = ? AND status = 1 OR status = 2 OR status= 6", carnet)


    historial = []

    for item in ver_press(carnet, 0):
        historial.append(item)

    return render_template('ulogin.html', historial=historial, activos=activos)




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route('/perfil', methods=["GET", "POST"])
@login_required
def perfil():
    carnet = session["carnet"]

    estudiante = db.execute('SELECT * FROM usuarios WHERE carnet = ?', carnet)[0]


    #ucarrera = estudiante["carrera"]
    carreras = unicarreras()
    carreras.remove(estudiante["carrera"])
    if request.method == "POST":

        if request.form.get("pasw") != request.form.get("confpasw"):
            return apology("Las contraseñas deben coincidir")



        nombres = request.form.get("nombre")
        apellidos = request.form.get("apellido")
        correo = request.form.get("correo")
        hash = generate_password_hash(request.form.get("pasw"))
        carrera = request.form.get("carrera")
        numero = request.form.get("telefono")

        if re.fullmatch(pat_celular, numero):
            caracteres = "+- "
            for a in range(len(caracteres)):
                numero = numero.replace(caracteres[a], "")
        else:
            return apology("Ingrese un numero de celular valido",403)

        celular = int(numero)

        db.execute("UPDATE usuarios SET nombres = ?, apellidos = ?, email = ?, hash = ?, carrera = ?, telefono =?  WHERE carnet = ? ",
                   nombres,apellidos,correo,hash,carrera,celular,carnet)
        flash("Perfil actualizado con exito")
        return redirect(url_for('usuariohome'))



    return render_template('perfil.html', carnet=carnet, estudiante=estudiante, carreras=carreras)


@app.route('/administrador', methods=["GET", "POST"])
@admin_required
def admin():

    aver = tramites()
    return render_template('admin.html', tramites=aver)




@app.route('/aprobar-prestamo', methods=["POST"])
def aprobando():
    id_prestamos = request.form.get("q")
    ver = db.execute("SELECT * from prestamo inner join libros on (prestamo.libro_id = libros.id_libro) where prestamo.id_prestamo = ?", id_prestamos)
    return render_template('aprobando.html', libro=ver[0])

@app.route('/prestamo-aprobado', methods=["POST"])
def aprobar_prestamo():
    trabajador = session["id_trabajador"]
    id_prestamos = request.form.get("q")

    ver = db.execute("SELECT * from prestamo inner join libros on (prestamo.libro_id = libros.id_libro) where prestamo.id_prestamo = ?", id_prestamos)
    id_libro = ver[0]["libro_id"]
    db.execute("UPDATE prestamo SET status = 1 WHERE id_prestamo = ?", id_prestamos)
    db.execute("UPDATE prestamo SET trabajador_id = ? WHERE id_prestamo = ?", trabajador, id_prestamos)
    db.execute("UPDATE inventario SET estado = 1 WHERE libro_id = ?", id_libro)
    return "Prestamo aprobado"

@app.route('/denegar-prestamo', methods=["POST"])
def denegar_prestamo():
    trabajador = session["id_trabajador"]
    id_prestamos = request.form.get("q")

    ver = db.execute("SELECT * from prestamo inner join libros on (prestamo.libro_id = libros.id_libro) where prestamo.id_prestamo = ?", id_prestamos)
    db.execute("UPDATE prestamo SET status = 5 WHERE id_prestamo = ?", id_prestamos)
    return "Prestamo denegado"


@app.route('/busqueda', methods=["GET", "POST"])
@login_required
def busqueda():
    if request.method == "POST":
        busqueda = []
        q = request.form.get("inputbusqueda")
        for item in buscar_libro(q):
            busqueda.append(item)

        return render_template('tabla.html', historial=busqueda)
    else:
        return render_template('buscador.html')


# URLS de consultaas

@app.route("/libros-resultados", methods = ["POST"])
def libros_resultados():
    q = request.form.get("q")

    datos = []

    libros = db.execute("SELECT * FROM libros where titulo like ? OR AUTOR like ? or descriptor like ?  GROUP BY titulo", "%"+q+"%", "%"+q+"%", "%"+q+"%")


    for i in libros:
        datos.append({"titulo":i["titulo"]})

     # where autor  = q or nombre = q

    return jsonify(datos)


@app.route("/libros-info", methods = ["POST"])
def libros_info():
    q = request.form.get("q")

    libros = db.execute("SELECT * FROM libros WHERE id_libro = ?", q)

    return render_template("info-libro.html", libro=libros[0])

@app.route("/solicitud-sala", methods = ["POST"])
def solicitud_sala():
    carnet = session["carnet"]
    isbn = request.form.get("isbn")
    id_libro = request.form.get("id_libro")
    verificadores = [verificar_vencido(carnet),
                     contar_libros(isbn),
                     verificar_nolotenga(carnet, isbn),
                     verificar_tramitesala(carnet, isbn)]

    if False not in verificadores:

        db.execute("INSERT INTO prestamo (fecha_prestamo, libro_id, u_carnet, fecha_devolucion, status) VALUES (?,?,?,?,?)",date.today(), id_libro, carnet, fecha_prestamo(),4 )
        return "Prestamo solicitado",200
        #Haciendo el update
    else:
        return "Prestamo Sala No se puede hacer el prestamo en este momento",400


@app.route("/solicitud_domicilio", methods = ["POST"])
def solicitud_domicilio():
    carnet = session["carnet"]
    isbn = request.form.get("isbn")
    id_libro = request.form.get("id_libro")
    verificadores = [verificar_vencido(carnet),
                     verificar_disponibles(isbn),
                     verificar_enprestamo(carnet),
                     verificar_nolotenga(carnet, isbn),
                     verificar_entramite(carnet, isbn)
                     ]


    if False not in verificadores:

        db.execute("INSERT INTO prestamo (fecha_prestamo, libro_id, u_carnet, fecha_devolucion, status) VALUES (?,?,?,?,?)",date.today(), id_libro, carnet, date.today(),4 )
        return "Prestamo solicitado",200
        #Haciendo el update
    else:
        return "No se puede hacer el prestamo en este momento",400


@app.route('/libros', methods=["POST", "GET"])
@admin_required
def administrar_libros():
    if request.method == "POST":
        if not request.form.get("cantidad"):
            return apology("Ingrese la cantidad de libros")
        if not request.form.get("titulo"):
            return apology("Ingrese el titulo del libro")
        if not request.form.get("autor"):
            return apology("Introduzca el autor del libro")
        if not request.form.get("clasificacion"):
            return apology("Ingrese el titulo del libro")
        if not request.form.get("confirmar"):
            return apology("Confirme la cantidad de libros")

        if request.form.get("cantidad") != request.form.get("confirmar"):
            return apology("Confirme que la cantidad y la confirmacion sea la misma")
        else:
            qty = confirmar_numerico(request.form.get("cantidad"))

        conf_edicion = confirmar_numerico(request.form.get("edicion"))
        if conf_edicion is False:
            return apology("Ingrese solo numeros")

        agregar_libros(int(request.form.get("cantidad")),request.form.get("isbn"),request.form.get("titulo"),request.form.get("autor"),request.form.get("year"),request.form.get("clasificacion"),request.form.get("descriptor"),request.form.get("edicion"),request.form.get("imagen"),request.form.get("editorial"))
        flash("Ingresado ")








    return render_template('libros.html')

@app.route('/devolver_libro', methods=["GET"])
def devolver():

    print("Devolviendo")
    id_libro  = request.args.get("libro")
    db.execute("UPDATE prestamo SET status = 7 WHERE id_prestamo = ?", id_libro)
    return redirect(url_for("usuariohome"))



# Devolver o Renovar Hacer la ruta que reciba por get
# Usando request.args.get("nombredelavariable") )(en renovar se llama libro)
# con eso hacer toda la renovacion y returnar un redirect a la ruta principal "/"