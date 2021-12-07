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
from model.misc import chooseCity
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

        print('='*3,'Airports-Routes DiGraph','='*3)
        print('Vertices: ', gr.numVertices(catalog['dir_connections']))
        print('Arcos', gr.numEdges(catalog['dir_connections']))

        print('='*3,'Airports-Routes Graph','='*3)
        print('Vertices: ', gr.numVertices(catalog['dual_connections']))
        print('Arcos', gr.numEdges(catalog['dual_connections']))

        print('El total de ciudades cargadas es de: ', mp.size(catalog['cities']))
        print('Informacion de los primeros aeropuertos cargados a los grafos: ')
        firstdir=mp.get(catalog['airports'], ctr[2])['value']
        table=pt.PrettyTable(hrules=pt.ALL)
        table.field_names=['Name','City','Country','Latitude','Longitude','Grafo']
        table.add_row([ctr[1]['Name'],ctr[1]['City'],ctr[1]['Country'],round(float(ctr[1]['Latitude']),2),round(float(ctr[1]['Longitude']),2),'Dirigido'])
        table.add_row([firstdir['Name'],firstdir['City'],firstdir['Country'],round(float(firstdir['Latitude']),2),round(float(firstdir['Longitude']),2),'No dirigido'])
        print(table)

        print('Informacion de la ultima ciudad cargada:')
        table2=pt.PrettyTable(hrules=pt.ALL)
        table2.field_names=['City','Population','Latitude','Longitude']
        table2.add_row([ctr[3]['city_ascii'],ctr[3]['population'],round(float(ctr[3]['lat']),2),round(float(ctr[3]['lng']),2)])
        print(table2)
    elif int(inputs[0]) == 2:#Req1
        result=controller.findInterconected(catalog)
        top=lt.subList(result,1,5)
        print('='*7,'Req No. 1 Inputs','='*7)
        print('Most connected airports in network (TOP 5)')
        print('Number of airports in network: ', gr.numVertices(catalog['dir_connections']))
        
        
        print('\n='*7,'Req No. 1 Answers','='*7)
        print('Connected airports inside of network: ', lt.size(result))
        table=pt.PrettyTable(hrules=pt.ALL)
        table.field_names=['Name','City','Country','IATA','Connections','Inbound','Outbound']
        for a in lt.iterator(top):
            info=mp.get(catalog['airports'],a['Airport'])['value']
            table.add_row([info['Name'],info['City'],info['Country'],info['IATA'],a['Interconnections'],a['Inbound'],a['Outbound']])
        print('Top 5 most connected airports...\n')    
        print(table)    
        
    elif int(inputs[0]) == 3:#Req2
        print(controller.req2(catalog, input("Iata 1: "), input("Iata 2: ")))
    elif int(inputs[0]) == 4:#Req3
        origin=input('Ciudad de salida: ')
        destiny=input('Ciudad de llegada: ')
        origin_city=mp.get(catalog['cities'],origin)['value']
        destiny_city=mp.get(catalog['cities'],destiny)['value']

        if lt.size(origin_city)>1:
            chooseCity(origin_city)
            ocity_opt=int(input('Varias ciudades encontradas bajo el mismo nombre, seleccione una opcion:'))
            selected_ocity=lt.getElement(origin_city,ocity_opt)
        else:
            selected_ocity=lt.firstElement(origin_city)

        if lt.size(destiny_city)>1:
            chooseCity(destiny_city)
            dcity_opt=int(input('Varias ciudades encontradas bajo el mismo nombre, seleccione una opcion:'))
            selected_dcity=lt.getElement(destiny_city,dcity_opt)
        else:
            selected_dcity=lt.firstElement(destiny_city)
        result=controller.req3(catalog,selected_ocity,selected_dcity)

        print('Aeropuerto de Origen: ')
        print('Aeropuerto de Salida: ')

        print(result)
    elif int(inputs[0]) == 5:#Req4
        city=input('Ingrese la ciudad de origen: ')
        miles=float(input('Ingrese la cantidad de millas disponibles: '))*1.6
        ocity=mp.get(catalog['cities'],city)['value']
        print('1',city)
        if lt.size(ocity)>1:
            chooseCity(ocity)
            ocity_opt=int(input('Varias ciudades encontradas bajo el mismo nombre, seleccione una opcion:'))
            selected_city=lt.getElement(ocity,ocity_opt)
        else:
            selected_city=lt.firstElement(ocity)
        airport, connected_airport, total_distance, final_path, longest = controller.req4(catalog, selected_city, miles)

        print('='*7,'Req No. 4 Inputs','='*7)
        print('Departure city name: ', city)
        print('Available travel miles: ',miles/1.6,'\n') #Convertidas a km
        print('='*7,'Req No. 4 Answer','='*7)
        print('Departure airport information: ')
        table=pt.PrettyTable(hrules=pt.ALL)
        table.field_names=['IATA','Name','City','Country']    
        table.add_row([airport['IATA'],airport['Name'],airport['City'],airport['Country']])
        print(table)

        print('-Number of possible airports:',connected_airport)
        print('-Max traveling distance between airports:', round(total_distance,2),'(km)')
        print('-Available traveling miles:', miles,'(km)\n')
        
        print('+++ Longest possible route with airport: ',airport['IATA'],'+++')
        print('- Longests possible path distance: ',round(float(longest),2)*2,'(km) back and forth from the destination.')
        print('- Longest possible path details: ')
        table2=pt.PrettyTable(hrules=pt.ALL)
        table2.field_names=['Departure','Destination','Distance (km)']
        for a in lt.iterator(final_path):
            table2.add_row([a['vertexA'],a['vertexB'],round(a['weight'],2)])
        print(table2)
        print('-'*5)
        if longest>miles:
            print('The passenger needs ', round(longest*2-miles,2),'miles to complete the trip.')
        else:
            print('The passenger CAN complete the trip with available miles. ')
        print('-'*5)
    elif int(inputs[0]) == 6:#Req5
        pass

    else:
        sys.exit(0)
