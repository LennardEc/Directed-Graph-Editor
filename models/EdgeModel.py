class EdgeModel:
    """
    The EdgeModel class is a data model implementation. 

    The model is (primarily) responsible for the logic of the application.


    The EdgeModel class constructor takes 3 parameters:
        start:   vertex that the edge is outgoing
        end:     vertex the edge is ingoing
        eight:   weight of the edge with a default value of 1.0

        Example: edge = Edge("A", "B", 1.2)

    The EdgeModel provides 3 methods:
        toString: edge.toString()
                                        returns the string representation

        isStartVertex: edge.isStartVertex(start)
                                        returns true if the given vertex name is the start vertex otherwise false

        isEndVertex: edge.isEndVertex(end)
                                        returns true if the given vertex name is the end vertex otherwise false
    """


    def __init__(self, start, end, weight=1.0):
        self.start = start
        self.end = end
        self.weight = weight
        
    def __eq__(self, other):
        if not isinstance(other, EdgeModel):
            return NotImplemented
        return self.start == other.start and self.end == other.end and self.weight == other.weight

    def toString(self):
        return self.start + "->" + self.end
    
    def isStartVertex(self, start):
        return self.start == start


    def isEndVertex(self, end):
        return self.end == end