from DISClib.Algorithms.Graphs.dijsktra import Dijkstra, pathTo, distTo

def shortCityPath(catalog, city1, city2):
    dijsktra = Dijkstra(catalog['dir_connections'], city1)
    return pathTo(dijsktra, city2), distTo(dijsktra, city2)

    