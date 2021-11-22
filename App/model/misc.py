from DISClib.ADT.graph import gr

def safeInsertVertex(graph, vertex):
    if not gr.containsVertex(graph, vertex):
        gr.insertVertex(graph, vertex)

def safeAddEdge(graph, vertex1, vertex2, weigth, type):
    if gr.getEdge(graph, vertex1, vertex2) is None:
        print("Added edge:", vertex1, vertex2, "to graph", type)
        gr.addEdge(graph, vertex1, vertex2, weigth)