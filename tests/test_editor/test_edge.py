import pytest
from models.GraphModel import GraphModel

graphModel = GraphModel('New')


def test_add_edge():
    graphModel.addVertex('A')
    graphModel.addVertex('B')
    graphModel.addEdge('A', 'B')
    edgeList = graphModel.getEdgeListOfVertex('A')
    edge = edgeList[0]
    assert edge.start == 'A'
    assert edge.end == 'B'
    assert edge.weight == 1.0
    graphModel.deleteVertex('A')
    graphModel.deleteVertex('B')



def test_delete_edge():
    graphModel.addVertex('A')
    graphModel.addVertex('B')
    graphModel.addEdge('A', 'B')
    edgeList = graphModel.getEdgeListOfVertex('A')
    edge = edgeList[0]
    assert edge.start == 'A'
    graphModel.deleteEdge('A', 'B')
    edgeList = graphModel.getEdgeListOfVertex('A')
    assert len(edgeList) == 0
    graphModel.deleteVertex('A')
    graphModel.deleteVertex('B')

