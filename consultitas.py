from objs import Libro, ver_press

#l = Libro(1)

historial = []

for item in ver_press(20190881, 0):
    print(item)
    historial.append(item)


print(historial[0]["id_prestamo"])
print(historial[0])
print("Id \t Titulo \t\t  Autor \t fecha")
for a in historial:
   print(a["id_prestamo"], a["libro"], a["autor"], "\t", a["fecha_prestamo"])

print(len(historial))
