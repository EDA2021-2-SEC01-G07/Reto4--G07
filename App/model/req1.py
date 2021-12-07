import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr

assert cf

def findInterconected(catalog):
    interconnections=lt.newList(datastructure="ARRAY_LIST")

    vertex= gr.vertices(catalog['dir_connections'])
    for a in lt.iterator(vertex):
        inter = 0
        inter= gr.indegree(catalog['dir_connections'],a) + gr.outdegree(catalog['dir_connections'],a)
        if inter==0:
            continue
        info={'Airport':a, "Interconnections": inter,'Inbound': gr.indegree(catalog['dir_connections'],a), 'Outbound':gr.outdegree(catalog['dir_connections'],a) }
        lt.addLast(interconnections,info)
    ms.sort(interconnections, lambda port1, port2: port1['Interconnections']>port2['Interconnections'])
    return interconnections