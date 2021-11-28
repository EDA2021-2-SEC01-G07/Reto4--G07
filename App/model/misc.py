from haversine.haversine import Direction
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
import haversine
from DISClib.ADT import orderedmap as om
import prettytable as pt

def safeInsertVertex(graph, vertex):
    if not gr.containsVertex(graph, vertex):
        gr.insertVertex(graph, vertex)

def safeAddEdge(graph, vertex1, vertex2, weigth):
    if gr.getEdge(graph, vertex1, vertex2) is None:
        gr.addEdge(graph, vertex1, vertex2, weigth)

def cityToAirport(catalog,city):
    """
    City: es el diccionario de una sola ciudad ya seleccionada previamente
    Se busca cual es el aeropuerto mas cercano a City y se retorna el aeropuerto"""
    lat_tree = catalog['latitude']
    coords= (float(city['lat']), float(city['lng']))
    d=10
    
    filtered_list = lt.newList(datastructure='ARRAY_LIST')

    while lt.size(filtered_list) == 0:
        n = haversine.inverse_haversine(coords,d,Direction.NORTH)
        s = haversine.inverse_haversine(coords,d,Direction.SOUTH)
        w = haversine.inverse_haversine(coords,d,Direction.WEST)
        e = haversine.inverse_haversine(coords,d,Direction.EAST)
        
        lat_airports = om.values(lat_tree, s[0], n[0])
        for list in lt.iterator(lat_airports):
            for airport in lt.iterator(list):
                if float(airport['Longitude']) > w[1] and float(airport['Longitude']) < e[1]:
                    lt.addLast(filtered_list,airport)
        d+=10

    if lt.size(filtered_list)!=1:
        for b in lt.airport(filtered_list):
            airport_coords=(float(b['Latitude']), float(b['Longitude']))
            distance=haversine.haversine(coords,airport_coords)
            if distance < d:
                airport = b
                d=distance
    else:
        airport = lt.firstElement(filtered_list)
    return airport, d

def chooseCity(city):
    table=pt.PrettyTable(hrules=pt.ALL)
    table.field_names=['Option','City','Country','Subregion','Latitude','Longitude']
    opt=1
    for c in lt.iterator(city):    
        table.add_row([opt,c['city_ascii'],c['country'],c['admin_name'],c['lat'],c['lng']])
        opt+=1
    
    print(table)
    