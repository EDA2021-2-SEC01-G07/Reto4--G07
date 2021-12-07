import sys
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from model.misc import cityToAirport
import DISClib.Algorithms.Graphs.prim as pr
import DISClib.Algorithms.Graphs.dijsktra as djk

def Millas(catalog, city, miles):
    """
    Se hace dijkstra al aeropuerto seleccionado. 
    Luego se recorren todos los vertices del grafo y se mira si hay via y la distancia
    Returns:
        Airport: El aeropuerto de salida
        connected_airport: Numero de aeropuertos conectados al aeropuerto incial
        total_distance: La distancia total del arbol de expansion minima
        final_path: El camino (rama) mas larga que tiene el arbol de expansion
        longest: La distancia al aeropuerto mas lejano.
    """

    airport=cityToAirport(catalog, city)[0]
    connected_airport=0
    total_distance=0
    longest=0
    dijkstra = djk.Dijkstra(catalog['dir_connections'],airport['IATA'])
    edges = gr.vertices(catalog['dir_connections'])
    
    pr.initSearch()
    for e in lt.iterator(edges):
        if djk.hasPathTo(dijkstra,e) == True:
            connected_airport+=1
            distance=float(djk.distTo(dijkstra,e))
            total_distance+=distance
            jumps=lt.size(djk.pathTo(dijkstra,e))
            if jumps>longest:
                longest=jumps
                destination=e
                destination_dist=distance
    print(djk.pathTo(dijkstra,'AZN'))
    final_path=djk.pathTo(dijkstra,destination)
    # djk.distTo()
    # djk.hasPathTo()----------True/false
    # djk.pathTo()
    return airport, connected_airport, total_distance, final_path, destination_dist