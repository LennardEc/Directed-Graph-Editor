import pytest
from models.GraphModel import GraphModel

graphModel = GraphModel('New')


def test_add_vertex():
    graphModel.addVertex('A')
    vertex = graphModel.getVertex('A')
    graphModel.deleteVertex('A')
    assert vertex.name == 'A'


def test_validate_vertex():
    graphModel.addVertex('A')
    is_there = graphModel.validateVertex('A')
    graphModel.deleteVertex('A')
    assert is_there == True


def test_delete_vertex():
    graphModel.addVertex('A')
    is_there = graphModel.validateVertex('A')
    graphModel.deleteVertex('A')
    is_still_there = graphModel.validateVertex('A')
    assert is_there == True
    assert is_still_there == False


def test_get_vertex_names():
    graphModel.addVertex('A')
    names = graphModel.getVertexNames()
    graphModel.deleteVertex('A')
    assert names[0] == 'A'
