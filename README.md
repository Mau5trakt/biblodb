# Biblodb
<img src="https://badgen.net/github/tag/mau5trakt/biblodb">  <img src="https://badgen.net/github/open-issues/mau5trakt/biblodb">  <img src="https://badgen.net/github/branches/mau5trakt/biblodb">
 <br>	<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"> 
 <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white">
 <img src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white">

## Tabla de contenido
1. [Resumen](#resumen)
2. [Inicio Rapido](#inicio-rapido)
3. [Ramas](#ramas)
4. [Archivos Auxiliares](#archivos-auxiliares)
5. [Base de datos](#base-de-datos)
6. [Plantillas](#plantillas)
7. [Static](#static)
8. [Rutas](#rutas)

# Resumen
#### [Video Demo](https://youtu.be/rWBbmivxrPw)

<p> Biblodb es una aplicacion de para la gestion de una de biblioteca.  En la aplicacion el usuario se podra registrar, iniciar sesion, ver sus libros en prestamo actual y su historial de libros, buscar un libro y prestarlo para sala o domicilio.
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

## Ramas
<p> El proyecto cuenta con 2 ramas principales

- Master (Rama principal donde se aceptan las pull requests de otras ramas o se hacen commits directos si son hotfixes)
- Develop (Rama de desarrollo donde se crean nuevas funcionalidades, se corrigen existenten y se prueban antes de ser enviados a Master)
</p>

## Archivos Auxiliares

<p>Con el proposito de tener un codigo lo mas limpio posible, las funciones largas, contienen consultas sql o se usan muchas veces en la aplicacion fueron desarrolladas en el archivo functions.py y se importan en app.py, Asimismo, se hace uso de funciones auxiliares las cuales se encuentran en helpers.py (imagen con mensaje y hacer la sesion del usuario)
 </p>

## Base de datos
<p> El manejo de la base de datos se hace a traves del modulo SQL de la libreria CS50. 

## Plantillas
<p> el motor de plantillas pde este proyecto es jinja 2. se provee de una estructura base en el archivo templates/layout.html

## Static
 La gestion de los archivos estatico se da en esta carpeta, la cual contiene:
  - busqueda.js (Script con las funciones en javascript para el proyecto)
  - favicon.ico (Icono favicon del sitio)
  - history.png (Icono png, no se usa )
  - pattern.png (Imagen de fondo para el sitio)
  - style.css (Estilos css usados en el sitio)
  - user.png (Icono para el link del perfil, no se usa)
  
## Rutas
describir las rutas de la aplicacion
  
