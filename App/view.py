﻿"""
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
import time
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
        start_time = time.process_time()
        catalog=controller.newCatalog()
        ctr=controller.loadData(catalog)
        end_time=(time.process_time() - start_time)*1000
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
        print("The processing time is: ",end_time, " ms.")
    elif int(inputs[0]) == 2:#Req1
        start_time = time.process_time()
        result=controller.findInterconected(catalog)
        top=lt.subList(result,1,5)
        end_time=(time.process_time() - start_time)*1000
        print('='*7,'Req No. 1 Inputs','='*7)
        print('Most connected airports in network (TOP 5)')
        print('Number of airports in network: ', gr.numVertices(catalog['dir_connections']))
        
        
        print('='*7,'Req No. 1 Answers','='*7)
        print('Connected airports inside of network: ', lt.size(result))
        table=pt.PrettyTable(hrules=pt.ALL)
        table.field_names=['Name','City','Country','IATA','Connections','Inbound','Outbound']
        for a in lt.iterator(top):
            info=mp.get(catalog['airports'],a['Airport'])['value']
            table.add_row([info['Name'],info['City'],info['Country'],info['IATA'],a['Interconnections'],a['Inbound'],a['Outbound']])
        print('Top 5 most connected airports...\n')    
        print(table)    
        print("The processing time is: ",end_time, " ms.")
    elif int(inputs[0]) == 3:#Req2
        iatat1=input('Iata code 1: ')
        iatat2=input('Iata code 2: ')
        start_time = time.process_time()
        result=controller.req2(catalog, iatat1, iatat2)
        end_time=(time.process_time() - start_time)*1000

        print('='*7,'Req No. 2 Inputs','='*7)
        print('Airport-1 IATA Code:', iatat1)
        print('Airport-2 IATA Code:', iatat2)

        print('='*7,'Req No. 2 Answer','='*7)
        print('+'*3, 'Airport1 IATA Code:', iatat1,'+'*3)
        airport1=mp.get(catalog['airports'],iatat1)['value']
        table1=pt.PrettyTable(hrules=pt.ALL)
        table1.field_names=['IATA','Name','City','Country']
        table1.add_row([airport1['IATA'],airport1['Name'],airport1['City'],airport1['Country']])
        print(table1,'\n')

        print('+'*3, 'Airport2 IATA Code:', iatat2,'+'*3)
        airport2=mp.get(catalog['airports'],iatat2)['value']
        table2=pt.PrettyTable(hrules=pt.ALL)
        table2.field_names=['IATA','Name','City','Country']
        table2.add_row([airport2['IATA'],airport2['Name'],airport2['City'],airport2['Country']])
        print(table2,'\n')

        print('- Number of SCC in Airport-Route network:', result[0])
        print('- Does the',airport1['Name'],'and the', airport2['Name'],'belong together?')
        print('- AND:', result[1])
        print("The processing time is: ",end_time, " ms.")
    elif int(inputs[0]) == 4:#Req3
        origin=input('Ciudad de salida: ')
        destiny=input('Ciudad de llegada: ')
        origin_city=mp.get(catalog['cities'],origin)['value']
        destiny_city=mp.get(catalog['cities'],destiny)['value']
        visited=lt.newList(datastructure="ARRAY_LIST")
        last=''
        if lt.size(origin_city)>1:
            chooseCity(origin_city)
            ocity_opt=int(input('Varias ciudades encontradas bajo el mismo nombre, seleccione una opcion: '))
            selected_ocity=lt.getElement(origin_city,ocity_opt)
        else:
            selected_ocity=lt.firstElement(origin_city)

        if lt.size(destiny_city)>1:
            chooseCity(destiny_city)
            dcity_opt=int(input('Varias ciudades encontradas bajo el mismo nombre, seleccione una opcion:'))
            selected_dcity=lt.getElement(destiny_city,dcity_opt)
        else:
            selected_dcity=lt.firstElement(destiny_city)
        
        start_time = time.process_time()
        path, distance, airport1, airport2=controller.req3(catalog,selected_ocity,selected_dcity)
        end_time=(time.process_time() - start_time)*1000
        print('='*7,'Req No. 3 Inputs','='*7)
        print('Departure city:', origin)
        print('Arrival city:', destiny)

        print('='*7,'Req No. 3 Answer','='*7)
        print('+'*3, 'The departure airport in',origin, 'is:')
        table1=pt.PrettyTable(hrules=pt.ALL)
        table1.field_names=['IATA','Name','City','Country']
        table1.add_row([airport1['IATA'],airport1['Name'],airport1['City'],airport1['Country']])
        print(table1,'\n')

        print('+'*3, 'The arrival airport in',destiny, 'is:')
        table2=pt.PrettyTable(hrules=pt.ALL)
        table2.field_names=['IATA','Name','City','Country']
        table2.add_row([airport2['IATA'],airport2['Name'],airport2['City'],airport2['Country']])
        print(table2,'\n')

        print('+'*3, "Dijkstra's Trip Details",'+'*3)
        print('- Total distance (including city to airport):', distance)
        print('- Trip path: ')
        table3=pt.PrettyTable(hrules=pt.ALL)
        table3.field_names=['Departure','Destination','Distance (km)']
        for a in lt.iterator(path):
            table3.add_row([a['vertexA'],a['vertexB'],round(a['weight'],2)])
            lt.addLast(visited,a['vertexA'])
            lt.addLast(visited,a['vertexB'])
        print(table3)

        print('- Trip stops:')
        table4=pt.PrettyTable(hrules=pt.ALL)
        table4.field_names=['IATA','Name','City','Country']
        for b in lt.iterator(visited):
            if b==last:
                continue
            info=mp.get(catalog['airports'],b)['value']
            table4.add_row([info['IATA'],info['Name'],info['City'],info['Country']])
            last=b
        print(table4)
        print("The processing time is: ",end_time, " ms.")
    elif int(inputs[0]) == 5:#Req4
        city=input('Ingrese la ciudad de origen: ')
        miles=float(input('Ingrese la cantidad de millas disponibles: '))*1.6
        ocity=mp.get(catalog['cities'],city)['value']
        if lt.size(ocity)>1:
            chooseCity(ocity)
            ocity_opt=int(input('Varias ciudades encontradas bajo el mismo nombre, seleccione una opcion:'))
            selected_city=lt.getElement(ocity,ocity_opt)
        else:
            selected_city=lt.firstElement(ocity)

        start_time = time.process_time()

        airport, connected, final_path, weight = controller.req4(catalog, selected_city, miles)
        end_time=(time.process_time() - start_time)*1000

        print('='*7,'Req No. 4 Inputs','='*7)
        print('Departure city name: ', city)
        print('Available travel miles: ',miles/1.6,'\n') #Convertidas a km
        print('='*7,'Req No. 4 Answer','='*7)
        print('Departure airport information: ')
        table=pt.PrettyTable(hrules=pt.ALL)
        table.field_names=['IATA','Name','City','Country']    
        table.add_row([airport['IATA'],airport['Name'],airport['City'],airport['Country']])
        print(table)

        print('-Number of possible airports:', connected)
        print('-Max traveling distance between airports:', round(float(weight),2),'(km)')
        print('-Available traveling miles:', miles,'(km)\n')
        
        print('+++ Longest possible route with airport: ',airport['IATA'],'+++')
       
        last=''
        total_weight=0
        table2=pt.PrettyTable(hrules=pt.ALL)
        table2.field_names=['Departure','Destination','Distance (km)']
        for a in lt.iterator(final_path):
            if last != '':
                weight = gr.getEdge(catalog['dual_connections'], last, a)['weight']
                table2.add_row([last,a,round(float(weight),2)])
                total_weight += weight
            last = a
        print('- Longests possible path distance: ',round(float(total_weight),2)*2,'(km) back and forth from the destination or ', round(float(total_weight),2),'one way trip.')
        print('- Longest possible path details: ')
        print(table2)
        print('-'*5)

        if total_weight*2 > miles:
            print('The passenger needs ', round(total_weight*2/1.6 - miles/1.6,2),'miles to complete the trip.')
        else:
            print('The passenger CAN complete the trip with available miles. ')
        
        print('-'*5)
        print("The processing time is: ",end_time, " ms.")

    elif int(inputs[0]) == 6:#Req5
        start_time = time.process_time()
        iata = input('IATA code of closing airport: ')
        dir_edges, dir_size, dual_edges, dual_size, runnable = controller.req5(catalog,iata)
        end_time=(time.process_time() - start_time)*1000

        print('='*7,'Req No. 5 Inputs','='*7)
        print('Closing the airport with IATA code:',iata)
        print('\n--- Airports-Routes DiGraph ---')
        print('Original number of Airports:', gr.numVertices(catalog['dir_connections']), 'and edges:', gr.numEdges(catalog['dir_connections']))
        print('---','Airports-Routes Graph','---')
        print('Original number of Airports:', gr.numVertices(catalog['dual_connections']), 'and edges:', gr.numEdges(catalog['dual_connections']))
        
        print('\n+++ Removing the airport with IATA code:',iata,'+++')
        print('\n--- Airports-Routes DiGraph ---')
        print('Original number of Airports:', gr.numVertices(catalog['dir_connections'])-1, 'and edges:', int(gr.numEdges(catalog['dir_connections'])) - int(dir_size) )
        print('\n---','Airports-Routes DiGraph','---')
        print('Original number of Airports:', gr.numVertices(catalog['dual_connections'])-1, 'and edges:', int(gr.numEdges(catalog['dual_connections']))- int(dual_size) )

        print('='*7,'Req No. 5 Answers','='*7)
        print(f"There are {dir_size} airports affected by the removal of {iata}")
        print("The affected airports are:")
        table=pt.PrettyTable(hrules=pt.ALL)
        table.field_names = ['IATA', 'Name', 'City', 'Country']
        if lt.size(dir_edges) < 6:
            for b in lt.iterator(dir_edges):
                info = mp.get(catalog['airports'], b)['value']
                table.add_row([b, info["Name"], info["City"], info["Country"]])
        else:
            first = lt.subList(dir_edges, 1, 3)
            last = lt.subList(dir_edges, lt.size(dir_edges)-2, 3)
            for b in lt.iterator(first):
                info = mp.get(catalog['airports'], b)['value']
                table.add_row([b, info["Name"], info["City"], info["Country"]])
            for b in lt.iterator(last):
                info = mp.get(catalog['airports'], b)['value']
                table.add_row([b, info["Name"], info["City"], info["Country"]])
        print(table)
        print("\n\n"+str(runnable)+"\n\n")

        print("The processing time is: ",end_time, " ms.")
    else:
        sys.exit(0)
