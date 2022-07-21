class VertexModel:
    """
    The VertexModel class is a data model implementation. 

    The model is (primarily) responsible for the logic of the application.


    The EdgeModel class constructor takes 3 parameter:
        name:       name of the vertex
        source:     if the vertex is a source (default False)
        sink:       if the edge is a sink (default False)

    Example: vertex = Vertex("A", True, False)

    The VertexModel provides one method:
        toString: vertex.toString()
                                    returns the string representation
    """

    def __init__(self, name, source=False, sink=False):
        self.name = name
        self.source = source
        self.sink = sink
    
    def __eq__(self, other):
        if not isinstance(other, VertexModel):
            return NotImplemented
        return self.name == other.name and self.source == other.source and self.sink == other.sink

    def toString(self):
        return self.name