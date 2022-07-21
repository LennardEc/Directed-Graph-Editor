import random
from numpy.random import choice
import numpy as np


from utilities.CostumExceptions import DeadLock
from utilities.CostumExceptions import TraceLengthExceeded

class ProcessEngine:
    """
    A tool to generated traces based on a GraphModel.
    """
    def __init__(self, graph, minTrace, maxTrace):
        self.graph = graph
        self.minTrace = minTrace
        self.maxTrace = maxTrace

    def generateTrace(self):
        trace = []

        # get source to start
        possible_sources = self.graph.getSourceList()
        tmp_vertex = random.choice(possible_sources)
        trace.append(tmp_vertex.toString())

        is_sink = False

        # get all edges
        trace_length = 1
        while self.graph.hasNextEdge(tmp_vertex.toString()):
            possible_edges = self.graph.getEdgeListOfVertex(tmp_vertex.toString())

            scale_weights = 0.0
            weights = []
            for pe in possible_edges:
                tmp_weights = pe.weight
                scale_weights += tmp_weights
                weights.append(tmp_weights)

            tmp_edge = random.choice(choice(possible_edges,
                                            len(possible_edges),
                                            p=(np.array(weights) / scale_weights)))

            tmp_vertex_name = tmp_edge.end
            tmp_vertex = self.graph.getVertex(tmp_vertex_name)

            trace.append(tmp_vertex_name)

            trace_length += 1
            is_sink = tmp_vertex.sink
            # if min trace length reached and vertex is sink -> return trace
            if trace_length >= self.minTrace and is_sink:
                return trace

            # if max trace length reached -> raise error
            if self.maxTrace <= trace_length:
                raise TraceLengthExceeded("Maximal Trace length is exceeded")

        # if dead end is encountered either the last vertex is a sink then return trace else return error
        if len(trace) >= self.minTrace and is_sink:
            return trace
        else:
            raise DeadLock("Engine encountered dead lock")