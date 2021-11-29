import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
import DISClib.Algorithms.Graphs.prim as pr

def Millas(catalog):
    a=pr.PrimMST(catalog['dir_connections'])
    # print(a)
    # pr.edgesMST(catalog['dir_connections'])

    # pr.weightMST(catalog['dir_connections'])