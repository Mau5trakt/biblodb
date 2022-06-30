#from objs import ver_press, libros_disponibles
#from functions import ver_press, libros_disponibles, vencido
from datetime import timedelta, datetime, date
from functions import verificar_vencido, verificar_disponibles, verificar_enprestamo, verificar_nolotenga, fecha_prestamo

'''
verificadores = []
#Ver si tiene prestamos vencidos
ver1 = verificar_vencido("20190881")
verificadores.append(ver1)
#Ver si hay mas de 3 unidades de este libro
ver2 = verificar_disponibles(9789681863654)
verificadores.append(ver2)
#Ver si el usuario tiene mas de 3 prestamos activos
ver3 = verificar_enprestamo("20190881")
verificadores.append(ver3)

#ver que no sea el mismo libro
ver4 = verificar_nolotenga(20190881, 9789681863654)
verificadores.append(ver4)

print(verificadores)
if False in verificadores:
    print("No se puede realizar el prestamo")
#lista = [False,True, True]
'''
#print(str(date.today()))
'''
hoy = date.today()
agg = timedelta(days=7)
print(hoy + agg)
'''

print(type(fecha_prestamo()))

#semana = hoy + datetime.timedelta(days=7)


#hoy = datetime.strptime(str(date.today()), "%Y-%m-%d")
#semana = hoy + 7
#print(semana)


#if True in lista:
#    print("Falso")






