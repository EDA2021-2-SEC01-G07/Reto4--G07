from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr

def closedAirport(catalog, iata):
    edges = gr.adjacentEdges(catalog, iata)
    return edges, lt.size(edges)