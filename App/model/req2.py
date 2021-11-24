from DISClib.Algorithms.Graphs.scc import stronglyConnected, connectedComponents

def req2(catalog, iata1, iata2):
    return connectedComponents(catalog["kosaraju_connections"]), stronglyConnected(catalog["kosaraju_connections"], iata1, iata2)


