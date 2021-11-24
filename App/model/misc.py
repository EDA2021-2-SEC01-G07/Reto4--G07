from DISClib.ADT.graph import gr

def safeInsertVertex(graph, vertex):
    if not gr.containsVertex(graph, vertex):
        gr.insertVertex(graph, vertex)

def safeAddEdge(graph, vertex1, vertex2, weigth):
    if gr.getEdge(graph, vertex1, vertex2) is None:
        gr.addEdge(graph, vertex1, vertex2, weigth)