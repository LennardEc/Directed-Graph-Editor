class GraphModelChecker:
    """
    A class to check a GraphModel before saving, the first version implements only basic checking but the class
    can be extended with more complex and customized checking #todo mention in the report
    """

    def __init__(self, graph_model):
        self.model = graph_model

    def is_legal_graph(self):
        """
        Check if the GraphModel is legal.
        Returns either True or a pair with the error tag and the values
        """
        if self.source_and_sink():
            # if not empty the graph has disconnected sources
            not_connected = self.sinks_and_sources_are_connected()
            if not_connected:
                return False, "not_connected", not_connected

            # if not empty the graph has deadlocks
            deadlocks = self.deadlocks()
            if deadlocks:
                return False, "deadlocks", deadlocks

            return True
        else:
            return False, "Graph misses either a source or sink"

    def source_and_sink(self):
        """
        check if the model has at least on source and one sink
        """
        return self.model.hasSink() and self.model.hasSource()

    def deadlocks(self):
        """
        Identifies and report vertices that have no outgoing edges and are not a sink
        """
        dead_vertices = []
        for v in self.model.getVertexList():
            if not self.model.hasNextEdge(v.name) and (v.sink == False):
                dead_vertices.append(v.name)

        return dead_vertices

    def sinks_and_sources_are_connected(self):
        """
        Check that every source is connected to sink
        """
        sinks = self.model.getSinkList()
        sinks = [s.name for s in sinks]

        not_connected = []
        for source in self.model.getSourceList():
            visited = self.bfs([], [], source)
            if not any(v in sinks for v in visited):
                not_connected.append(source.name)

        return not_connected

    def bfs(self, visited, queue, node):
        visited.append(node.name)
        queue.append(node)

        while queue:
            s = queue.pop(0)
            for neighbour_edge in self.model.getEdgeListOfVertex(s.name):
                neighbour = self.model.getVertex(neighbour_edge.end)
                if neighbour.name not in visited:
                    visited.append(neighbour.name)
                    queue.append(neighbour)

        return visited
