from models.EdgeModel import EdgeModel
from models.VertexModel import VertexModel

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class GraphModel:
    """
    The GraphModel class is a data model implementation. 

    The model is (primarily) responsible for the logic of the application.
    """

    # build graph from a vertex and edge list
    def __init__(self, name, vertex_list=[], edge_list=[]):
        self.name = name
        self.graph = {}
        self.numberOfVertices = 0
        self.numberOfEdges = 0
        self.sources = []
        self.sinks = []
        self.vertexDict = {}

        for vertex in vertex_list:
            self.addVertex(vertex.toString(), vertex.source, vertex.sink)

        for edge in edge_list:
            self.addEdge(edge.start, edge.end, edge.weight)

    ##########################################################################################################################

    def validateVertex(self, name):
        return name in self.getVertexNames()

    def validateEdge(self, start_name, end_name, weight):
        return self.validateVertex(start_name) and self.validateVertex(
            end_name) and weight > 0.0 and not self.isEdge(start_name, end_name)

    # return true if an edge exists and false otherwise
    def isEdge(self, start, end):
        tmp = self.graph[start]
        return EdgeModel(start, end).toString() in tmp

    ########################################################################################################################

    def export(self):
        return list(self.vertexDict.values()), self.getEdgeList()

    #########################################################################################################################

    # adds a vertex to the graph. The function assumes that the name of the vertex is valid
    def addVertex(self, name, source=False, sink=False):
        vertex = VertexModel(name, source, sink)

        self.vertexDict[vertex.toString()] = vertex
        self.graph[vertex.toString()] = {}
        self.numberOfVertices += 1

        if vertex.source:
            self.sources.append(vertex)
        if vertex.sink:
            self.sinks.append(vertex)

    # adds an edge to the graph. The function assumes that both vertices exist and the weight is bigger than 0.0.
    def addEdge(self, start, end, weight=1.0):
        edge = EdgeModel(start, end, weight)

        if start in self.graph:
            tmp = self.graph[start]
            tmp[edge.toString()] = edge
        else:
            self.graph[start] = {edge.toString(): edge}

        self.numberOfEdges += 1

    ########################################################################################################################

    # removes an vertex either by passing a vertex object or the name
    def deleteVertex(self, vertex):
        vertex = self.vertexDict[vertex]

        if vertex.sink:
            vertex_to_delete = None
            for v in self.sinks:
                if v.name == vertex.name:
                    vertex_to_delete = v
            try:
                self.sinks.remove(vertex_to_delete)
            except:
                pass

        if vertex.source:
            vertex_to_delete = None
            for v in self.sources:
                if v.name == vertex.name:
                    vertex_to_delete = v
            try:
                self.sources.remove(vertex_to_delete)
            except:
                pass

        vertex_name = vertex.toString()
        edges = self.graph[vertex_name]

        self.vertexDict.pop(vertex_name)
        self.graph.pop(vertex_name)
        self.numberOfEdges -= len(edges)
        self.numberOfVertices -= 1

        tmp_graph = self.graph.copy()

        # iterate thorugh all vertices
        keys = self.getVertexNames()
        for tmp_vertex_name in keys:
            # edges of each vertex
            tmp_edges = tmp_graph[tmp_vertex_name]

            tmp_to_remove = []
            for tmp_edge in tmp_edges:
                # get edge
                tmp = tmp_edges[tmp_edge]
                # if the edge ends in the deleted vertex remove the edge
                if tmp.isEndVertex(vertex_name):
                    tmp_to_remove.append(tmp.toString())

            for ttr in tmp_to_remove:
                tmp_edges.pop(ttr)
                self.numberOfEdges -= 1

            tmp_graph[tmp_vertex_name] = tmp_edges

        self.graph = tmp_graph

    # an edge can be specified by either an object, start and end name and weight
    def deleteEdge(self, start, end):
        edge = EdgeModel(start, end, 1.0)

        edges = self.graph[edge.start]
        edges.pop(edge.toString())

        self.graph[edge.start] = edges
        self.numberOfEdges -= 1

    ##############################################################################################################

    # change the name of an existing vertex
    def modifyVertexName(self, name, new_name):
        # rename vertex
        vertex = self.vertexDict.pop(name)
        vertex_name = vertex.toString()
        vertex.name = new_name
        self.vertexDict[new_name] = vertex

        # rename outgoing edges
        edges = self.graph.pop(vertex_name)
        tmp_edges = edges.copy()
        tmp_res = {}
        for tmp_edge in tmp_edges:
            tmp = tmp_edges[tmp_edge]
            tmp.start = new_name
            tmp_res[tmp.toString()] = tmp

        self.graph[new_name] = tmp_res

        # rename ingoing edges
        # iterate thorugh all vertices
        tmp_graph = self.graph.copy()

        for tmp_vertex_name in self.getVertexNames():
            # edges of each vertex
            tmp_edges = tmp_graph[tmp_vertex_name]

            tmp_to_rename = []
            for tmp_edge in tmp_edges:
                # get edge
                tmp = tmp_edges[tmp_edge]
                # if the edge ends in the deleted vertex remove the edge
                if tmp.isEndVertex(vertex_name):
                    tmp_to_rename.append(tmp)

            for ttr in tmp_to_rename:
                rename = tmp_edges.pop(ttr.toString())
                rename.end = new_name
                tmp_edges[rename.toString()] = rename

            tmp_graph[tmp_vertex_name] = tmp_edges

        self.graph = tmp_graph

    def vertexChangeSource(self, name, source):
        tmp_vertex = self.vertexDict.pop(name)
        if source:
            tmp_vertex.source = source
            self.sources.append(tmp_vertex)
        else:
            try:
                tmp_vertex.source = source
                self.sources.remove(tmp_vertex)
            except:
                pass
        self.vertexDict[name] = tmp_vertex

    def vertexChangeSink(self, name, sink):
        tmp_vertex = self.vertexDict.pop(name)
        if sink:
            tmp_vertex.sink = sink
            self.sinks.append(tmp_vertex)
        else:
            tmp_vertex.sink = sink
            self.sinks.append(tmp_vertex)

        self.vertexDict[name] = tmp_vertex

    # change the weight of an existing edge
    def modifyEdge(self, start, end, weight):
        edge = EdgeModel(start, end, weight)
        start_edge_name = edge.start
        edges = self.graph[start_edge_name]

        tmp_edge = edges.pop(edge.toString())
        tmp_edge.weight = weight
        edges[edge.toString()] = tmp_edge
        self.graph[start_edge_name] = edges

    ##############################################################################################################

    def visualise(self):
        vertices, edges = self.export()

        G = nx.DiGraph()
        for vertex in vertices:
            G.add_node(vertex.toString())

        for edge in edges:
            G.add_edge(edge.start, edge.end, weight=edge.weight)

        #pos = nx.nx_pydot.pydot_layout(G, prog="fdp")
        pos = nx.spring_layout(G)

        fig, ax = plt.subplots()
        nx.draw_networkx_nodes(G, pos, ax=ax)
        nx.draw_networkx_labels(G, pos, ax=ax)

        curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
        straight_edges = list(set(G.edges()) - set(curved_edges))

        # angle of the arches
        arc_rad = 0.22

        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=straight_edges)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}')

        # make arch edges with the weight on it TODO

        edge_weights = nx.get_edge_attributes(G, 'weight')
        curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges}
        straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}

        my_draw_networkx_edge_labels(G, pos, ax=ax, font_size=7,
                                     edge_labels=curved_edge_labels, rotate=False, rad=arc_rad)

        nx.draw_networkx_edge_labels(G, pos, ax=ax, font_size=7,
                                     edge_labels=straight_edge_labels, rotate=False)

        name = self.name + "picture.png"
        plt.savefig(name, format='png', dpi=360)
        return name

    def getVertex(self, vertex_name):
        return self.vertexDict[vertex_name]

    # pass string
    def getEdgeListOfVertex(self, name):
        edges = self.graph[name]
        return list(edges.values())

    def hasNextEdge(self, name):
        return len(self.getEdgeListOfVertex(name)) > 0

    def getVertexList(self):
        return list(self.vertexDict.values())

    def getEdgeList(self):
        edge_list = []
        for key in self.graph:
            edges = self.graph[key]
            edge_list += list(edges.values())

        return edge_list

    def getSourceList(self):
        return self.sources.copy()

    def getSinkList(self):
        return self.sinks.copy()

    # return a list of strings containing all vertex names
    def getVertexNames(self):
        return [*self.vertexDict]

    def hasSource(self):
        return len(self.sources) > 0

    def hasSink(self):
        return len(self.sinks) > 0


"""
Helper function used to visualize the graph model
"""

def my_draw_networkx_edge_labels(G, pos, edge_labels=None, label_pos=0.5, font_size=10, font_color="k",
                                 font_family="sans-serif", font_weight="normal", alpha=None, bbox=None,
                                 horizontalalignment="center",
                                 verticalalignment="center", ax=None, rotate=True, clip_on=True, rad=0):
    if ax is None:
        ax = plt.gca()
    if edge_labels is None:
        labels = {(u, v): d for u, v, d in G.edges(data=True)}
    else:
        labels = edge_labels
    text_items = {}
    for (n1, n2), label in labels.items():
        (x1, y1) = pos[n1]
        (x2, y2) = pos[n2]
        (x, y) = (
            x1 * label_pos + x2 * (1.0 - label_pos),
            y1 * label_pos + y2 * (1.0 - label_pos),
        )
        pos_1 = ax.transData.transform(np.array(pos[n1]))
        pos_2 = ax.transData.transform(np.array(pos[n2]))
        linear_mid = 0.5 * pos_1 + 0.5 * pos_2
        d_pos = pos_2 - pos_1
        rotation_matrix = np.array([(0, 1), (-1, 0)])
        ctrl_1 = linear_mid + rad * rotation_matrix @ d_pos
        ctrl_mid_1 = 0.5 * pos_1 + 0.5 * ctrl_1
        ctrl_mid_2 = 0.5 * pos_2 + 0.5 * ctrl_1
        bezier_mid = 0.5 * ctrl_mid_1 + 0.5 * ctrl_mid_2
        (x, y) = ax.transData.inverted().transform(bezier_mid)

        if rotate:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < -90:
                angle += 180
            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(
                np.array((angle,)), xy.reshape((1, 2))
            )[0]
        else:
            trans_angle = 0.0
        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same

        t = ax.text(
            x,
            y,
            label,
            size=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            rotation=trans_angle,
            transform=ax.transData,
            bbox=bbox,
            zorder=1,
            clip_on=clip_on,
        )
        text_items[(n1, n2)] = t

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    return text_items
