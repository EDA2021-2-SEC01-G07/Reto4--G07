"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs.scc import KosarajuSCC
from model.misc import safeAddEdge, safeInsertVertex
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog={
        'dir_connections': None,
        'dual_connections': None,
        'airports':None
    }
    catalog['dir_connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                directed=True,
                                size=14000,
                                comparefunction=compareID)
    catalog['dual_connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                directed=False,
                                size=14000,
                                comparefunction=compareID)
    catalog['kosaraju_connections'] = {}
    catalog['latitude'] = om.newMap(omaptype="RBT", comparefunction=compareLatitude)
    catalog['airports'] = mp.newMap(3200, 
                                   maptype='CHAINING',
                                   loadfactor=3,
                                   comparefunction=compareAirportID)
    catalog['cities'] = mp.newMap(10500, 
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   comparefunction=compareCityName)
    return catalog
# Funciones para agregar informacion al catalogo
def addAirport(catalog, airport):
    """
    Añade los vertices a los grafos de aerolinea
        El nombre del vertice es el codigo IATA del aeropuerto
    Añade al diccionario airports la informacion de cada aeropuerto
        La llave es el IATA, el valor es toda la informacion
    """
    safeInsertVertex(catalog['dir_connections'],airport['IATA'])
    
    mp.put(catalog['airports'], airport['IATA'], airport)

    lat = round(float(airport["Latitude"]), 3)
    
    keyval = om.get(catalog["latitude"], lat)

    if keyval is None:
        airports = lt.newList()
        om.put(catalog["latitude"], lat, airports)
    else:
        airports = me.getValue(keyval)

    lt.addLast(airports, airport)

def addConnections(catalog, route):
    """
    Crea los arcos para los vertices en el grafo dirigido y en el no dirigido.
    """
    dgraph = catalog['dir_connections']
    sgraph = catalog['dual_connections']

    departure_node = route['Departure']
    destination_node = route['Destination']

    safeAddEdge(dgraph, departure_node, destination_node, route['distance_km'])

    if gr.getEdge(dgraph, destination_node, departure_node) is not None:
        safeInsertVertex(sgraph, departure_node)
        safeInsertVertex(sgraph, destination_node)
        safeAddEdge(sgraph, departure_node, destination_node, route['distance_km'])


def addCity(catalog,wcity):
    """
    Crea el mapa para ciudades
        La llave es el nombre de la ciudad, el valor es toda la info.
    """
    cities=catalog['cities']
    city_name=wcity['city_ascii']
    existCity = mp.contains(cities,city_name)
    if existCity:
        city=me.getValue(mp.get(cities,city_name))
    else:
        city=lt.newList("ARRAY_LIST")
        mp.put(cities,city_name,city)
    lt.addLast(city,wcity)
    

def loadStronglyConnected(catalog):
    catalog["kosaraju_connections"] = KosarajuSCC(catalog['dir_connections'])
# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# ==============================
# Funciones de Comparacion
# ==============================
def compareID(stat1, stat2):
    """
    Compara dos estaciones
    """
    dict_stat2 = stat2['key']
    if (stat1 == dict_stat2):
        return 0
    elif (stat1 > dict_stat2):
        return 1
    else:
        return -1

def compareAirportID(keyname,airID):
    """
    Compara dos id de aeropuertos
    """
    authentry = me.getKey(airID)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareCityName(keyname,city):
    """
    Compara dos nombres de ciudades.
    """
    authentry = me.getKey(city)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareLatitude(lat1, lat2):
    if (lat1 == lat2):
        return 0
    elif (lat1 > lat2):
        return 1
    else:
        return -1