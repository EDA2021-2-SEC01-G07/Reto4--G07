"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
default_limit = 1000 
sys.setrecursionlimit(default_limit*100)
from DISClib.ADT import map as mp
import prettytable as pt
from DISClib.ADT.graph import gr
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- (Req1) Encontrar puntos de interconexión aérea")
    print("3- (Req2) Encontrar clústeres de tráfico aéreo")
    print("4- (Req3) Encontrar la ruta más corta entre ciudades")
    print("5- (Req4) Utilizar las millas de viajero")
    print("6- (Req5) Cuantificar el efecto de un aeropuerto cerrado")

catalog = None

"""
Menu principal
"""
sys.setrecursionlimit(10000)
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog=controller.newCatalog()
        ctr=controller.loadData(catalog)
        print('Aeropuertos en el grafo dirigido: ', gr.numVertices(catalog['dir_connections']))
        print('Aeropuertos en el grafo no dirigido: ', gr.numVertices(catalog['dual_connections']))
        print('El total de ciudades cargadas es de: ', mp.size(catalog['cities']))
        print('Informacion de los primeros aeropuertos cargados a los grafos: ')
        firstdir=mp.get(catalog['airports'], ctr[2])['value']
        table=pt.PrettyTable(hrules=pt.ALL)
        table.field_names=['Name','City','Country','Latitude','Longitude']
        table.add_row([ctr[1]['Name'],ctr[1]['City'],ctr[1]['Country'],round(float(ctr[1]['Latitude']),2),round(float(ctr[1]['Longitude']),2)])
        table.add_row([firstdir['Name'],firstdir['City'],firstdir['Country'],round(float(firstdir['Latitude']),2),round(float(firstdir['Longitude']),2)])
        print(table)

        print('Informacion de la ultima ciudad cargada:')
        table2=pt.PrettyTable(hrules=pt.ALL)
        table2.field_names=['Population','Latitude','Longitude']
        table2.add_row([ctr[3]['population'],round(float(ctr[3]['lat']),2),round(float(ctr[3]['lng']),2)])
        print(table2)
    elif int(inputs[0]) == 2:#Req1
        result=controller.findInterconected(catalog)
        pass
    elif int(inputs[0]) == 3:#Req2
        print(controller.req2(catalog, input("Iata 1: "), input("Iata 2: ")))
    elif int(inputs[0]) == 4:#Req3
        city=mp.get(catalog['cities'],'Washington')
        
        # result=mc.cityToAirport(catalog,city)
        # print(result)
        pass
    elif int(inputs[0]) == 5:#Req4
        pass
    elif int(inputs[0]) == 6:#Req5
        pass

    else:
        sys.exit(0)
sys.exit(0)
