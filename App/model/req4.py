import sys
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from model.misc import cityToAirport
import DISClib.Algorithms.Graphs.prim as pr
import DISClib.Algorithms.Graphs.dfs as dfs
import DISClib.ADT.queue as q
import DISClib.ADT.stack as st
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
    longest=0
    final_path=None
    nodes=lt.newList(datastructure="ARRAY_LIST")

    prim_search = pr.PrimMST(catalog['dual_connections'])
    path = prim_search['mst']
    weight = pr.weightMST(catalog['dual_connections'], prim_search)
    
    # print(prim_search['edgeTo']['table'])
    
    while not q.isEmpty(path):
        edge = q.dequeue(path)
        if lt.isPresent(nodes, edge['vertexA'])==0:
            lt.addLast(nodes, edge['vertexA'])
        if lt.isPresent(nodes, edge['vertexB'])==0:
            lt.addLast(nodes, edge['vertexB'])
            
    connected=lt.size(nodes)
    
    df=dfs.DepthFirstSearch(catalog['dual_connections'],airport['IATA'])   
    for e in lt.iterator(nodes):
        if dfs.hasPathTo(df,e) == True:
            route = dfs.pathTo(df,e)      
            if st.size(route) > longest:
                final_path = route
                longest = st.size(route)

    #Da la misma longitud que el ejemplo, pero distinto vertice final
    return airport, connected, final_path, weight