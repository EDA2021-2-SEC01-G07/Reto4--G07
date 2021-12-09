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
import DISClib.Algorithms.Graphs.dfs as dfs
import DISClib.ADT.queue as q
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
    connected_airports=1
    total_distance=0
    longest=0   
    edges = gr.vertices(catalog['dir_connections'])
    # ==================================================================================================
    mst=pr.PrimMST(catalog['dual_connections'])
    
    df=dfs.DepthFirstSearch(catalog['dir_connections'],airport['IATA'])
    for e in lt.iterator(edges):
        if dfs.hasPathTo(df,e) == True:
            connected_airports += 1
            path_size = lt.size(dfs.pathTo(df,e))
            if path_size > longest:
                destination = e
                longest = path_size
    final_path=dfs.pathTo(df,destination)
    vertex_A=airport['IATA']
    for path in lt.iterator(final_path):
        connection=gr.getEdge(catalog['dir_connections'],vertex_A,path)
        if connection != None:
            total_distance+=connection['weight']
        vertex_A=path
        
    sys.exit(0)
    return airport, connected_airports, final_path, total_distance

    
    
    #=======================================================================================================

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

    final_path=djk.pathTo(dijkstra,destination)

    return airport, connected_airport, total_distance, final_path, destination_dist