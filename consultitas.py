from cs50 import SQL

db = SQL("sqlite:///database/respaldo.db")

sacar_id = db.execute("SELECT libro_id from prestamo where id_prestamo = 17")[0]["libro_id"]
print(sacar_id)
#Comentario
