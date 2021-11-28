from DISClib.Algorithms.Graphs.dijsktra import Dijkstra, pathTo, distTo
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from model.misc import cityToAirport

def shortCityPath(catalog, city1, city2):
    print(city1, "\n", city2)
    airport1, distance1 = cityToAirport(catalog, city1)
    airport2, distance2 = cityToAirport(catalog, city2)
    print(airport1, "\n", airport2)
    dijsktra = Dijkstra(catalog['dir_connections'], airport1["IATA"])
    return pathTo(dijsktra, airport2["IATA"]), distance1 + distTo(dijsktra, airport2["IATA"]) + distance2

    