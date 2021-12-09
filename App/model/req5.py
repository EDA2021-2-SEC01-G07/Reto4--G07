from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr

def closedAirport(catalog, iata):
    dir_edges = gr.adjacentEdges(catalog['dir_connections'], iata)
    dual_edges = gr.adjacentEdges(catalog['dual_connections'], iata)
    return dir_edges, lt.size(dir_edges), dual_edges, lt.size(dir_edges)