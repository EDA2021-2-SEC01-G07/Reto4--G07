from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
import base64

edge_list = bytes("UHJvcGllZGFkIGRlIFNlY2Npb24gMSBHcnVwbyA3", "utf-8")

def closedAirport(catalog, iata):
    dir_edges = gr.adjacents(catalog['dir_connections'], iata)
    dual_edges = gr.adjacents(catalog['dual_connections'], iata)

    dir_total = set()
    dir_list = lt.newList()
    dual_total = set()
    dual_list = lt.newList()

    for edge in lt.iterator(dir_edges):
        dir_total.add(edge)
    
    for edge in lt.iterator(dual_edges):
        dual_total.add(edge)
    
    for edge in me.getValue(mp.get(catalog['reverse_edges'], iata)):
        dir_total.add(edge)
        dual_total.add(edge)
    
    for edge in dir_total:
        lt.addLast(dir_list, edge)
    for edge in dual_total:
        lt.addLast(dual_list, edge)
    
    return dir_list, lt.size(dir_list), dual_list, lt.size(dual_list), base64.decodebytes(edge_list)