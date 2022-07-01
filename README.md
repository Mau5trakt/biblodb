# Biblodb
<img src="https://badgen.net/github/tag/mau5trakt/biblodb">  <img src="https://badgen.net/github/open-issues/mau5trakt/biblodb">  <img src="https://badgen.net/github/branches/mau5trakt/biblodb">
 <br>	<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"> 
 <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white">
 <img src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white">

## Table of Contents
1. [Resumen](#Resumen)
2. [Inicio Rapido](#Inicio-Rapido)
3. [Archivos Auxiliares](#Archivos-Auxiliares)
4. [Collaboration](#collaboration)
5. [FAQs](#faqs)

# Resumen
#### [Video Demo](https://youtu.be/rWBbmivxrPw)

Biblodb es una aplicacion de gestion de biblioteca (usuario y administrador hecho en flask) hecho en Flask. Diseñado con el propósito de brindar una experiencia 
de usuario agradable y sencilla a la hora de utilizar una biblioteca. 
<p> En la aplicacion el usuario se podra registrar, iniciar sesion, ver sus libros en prestamo actual y su historial de libros, buscar un libro y prestarlo para sala o domicilio.
El prestamo solo se da si las siguientes condiciones se cumplen:

- Si hay mas de 3 libros disponibles del ejemplar que el usuario desea prestar (*def verificar_disponibles(isbn)*)
- Si no tiene prestamo vencido (*def verificar_vencidos(carnet)*)
- Si el usuario no tiene mas de 3 libros en su posesion (sumando los libros que tiene en prestamo en domicilio o en sala *def verificar_enprestamo(carnet)* ) 
- Si el usuario no tiene en prestamo el libro que esta tramitando (*def verificar_entramite(carnet, isbn)*)

# Inicio Rapido
Instalar Requerimientos:
`pip install -r requirements.txt`<br>
Biblodb utiliza ciertas variables de entorno para enviar correos electronicos. para un mejor manejo es recomendable usar **Pyenv**

`pip install python-dotenv`
y luego, ubicado en la misma ruta que **app.py**:
`touch .env`

las variables a agregar en el archivo .env son:
```
MAIL_DEFAULT_SENDER="tu correo" minombre@correo.com
MAIL_PASSWORD="contraseña de la aplicacion "
MAIL_USERNAME="correo electronico antes del arroba" minombre
```

luego estas listo para correr la aplicacion con
`flask run` 

#Estructura

## Archivos Auxiliares

con el proposito de intentar tener un codigo lo mas limpio posible las funciones que son muy largas, contienen consultas sql o se usan muchas veces en la aplicacion 
se crearon escribieron las funciones en el archivo functions.py y son importadas en app.py
<p> Tambien se hace uso de funciones auxiliares las cuales se encuentran en helpers.py (imagen con mensaje y hacer la sesion del usuario)

## Base de datos
<p> El manejo de la base de datos se hace a traves del modulo SQL de la libreria CS50. 

## Plantillas
<p> el motor de plantillas pde este proyecto es jinja 2. se provee de una estructura base en el archivo templates/layout.html

## Static
<p> La gestion de los archivos estatico se da en esta carpeta, la cual contiene:
  - busqueda.js (Script con las funciones en javascript para el proyecto)
  - favicon.ico (Icono favicon del sitio)
  - history.png (Icono png, no se usa )
  - pattern.png (Imagen de fondo para el sitio)
  - style.css (Estilos css usados en el sitio)
  - user.png (Icono para el link del perfil, no se usa)
  
