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
from DISClib.ADT.graph import gr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog={
        'dir_connections': None,
        'strong_connections': None,
        'airports':None
    }
    catalog['dir_connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                directed=True,
                                size=14000,
                                comparefunction=compareID)
    catalog['strong_connections'] = gr.newGraph(datastructure='ADJ_LIST',
                            directed=False,
                            size=14000,
                            comparefunction=compareID)
    return catalog
# Funciones para agregar informacion al catalogo
def addAirport(catalog, airport):
    if not gr.containsVertex(catalog['dir_connections'],airport['IATA']):
        gr.insertVertex(catalog['dir_connections'],airport['IATA'])
    if not gr.containsVertex(catalog['strong_connections'],airport['IATA']):
        gr.insertVertex(catalog['strong_connections'],airport['IATA'])
def addConnections(catalog,route):
    
    gr.addEdge(catalog['dir_connections'], route['Departure'], route['Destination'], route['distance_km'])
    gr.addEdge(catalog['strong_connections'], route['Departure'], route['Destination'], route['distance_km'])
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