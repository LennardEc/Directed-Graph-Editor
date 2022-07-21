import os
import pytest
from utilities.FileManager import FileManager
from models.VertexModel import VertexModel
from models.EdgeModel import EdgeModel
from models.GraphModel import GraphModel
from models.LogModel import LogModel

@pytest.fixture(scope="module")
def vertex_list():
    vertexList =  [VertexModel("A", True), VertexModel("B"), VertexModel("C", False, True)]
    yield vertexList



@pytest.fixture(scope="module")
def edge_list ():
    edgeList = [EdgeModel("A", "B"), EdgeModel("B", "C")]
    yield edgeList

@pytest.fixture(scope="module")
def tmp_log():
    tmpLog =  [('3', ('register request', 'examine casually', 'check ticket', 'decide')), 
               ('2', ('register request', 'decide', 'pay compensation')), 
               ('1', ('register request', 'examine thoroughly', 'check ticket', 'decide', 'reject request'))
               ] 
    yield tmpLog

@pytest.fixture(scope="module")
def log_size():
    logSize = 3
    yield logSize 
    
@pytest.fixture(scope="module")
def noise_in_percent():
    noiseInPercent = 10
    yield noiseInPercent

@pytest.fixture(scope="module")
def distribution_of_noise():
    distributionOfNoise = (50, 30, 20)
    yield distributionOfNoise 
    
@pytest.fixture(scope="module")
def time_of_creation():
    timeOfCreation = "02.05.2022"
    yield timeOfCreation


@pytest.fixture(scope="module")
def graph_model_name():
    name = "graph_model_test"
    yield name

@pytest.fixture(scope="module")
def log_model_name():
    name = "log_model_test"
    yield name


@pytest.fixture(scope="module")
def file_manager_path():
    yield os.getcwd() + '/tests/resources/'

@pytest.fixture(scope="function")
def create_graph_model(graph_model_name, vertex_list, edge_list):
    graph_model = GraphModel(graph_model_name, vertex_list, edge_list)
    yield graph_model

@pytest.fixture(scope="function")
def create_log_model(log_model_name, tmp_log, graph_model_name, log_size, noise_in_percent, distribution_of_noise, time_of_creation):
    log_model = LogModel(log_model_name, tmp_log, graph_model_name, log_size, noise_in_percent, distribution_of_noise, time_of_creation) 
    yield log_model

@pytest.fixture(scope='function')
def create_file_manager(file_manager_path):
    file_manager = FileManager(file_manager_path)
    yield file_manager

@pytest.fixture(scope="function")
def create_graph_model(graph_model_name, vertex_list, edge_list):
    graph_model = GraphModel(graph_model_name, vertex_list, edge_list)
    yield graph_model



def test_load_model_names(create_file_manager):
    file_manager = create_file_manager
    model_size = len(file_manager.graphFiles)
    assert model_size == len(file_manager.loadModelNames())
    assert file_manager.graphFiles == file_manager.loadModelNames()

def test_load_log_names(create_file_manager):
    file_manager = create_file_manager
    log_size = len(file_manager.logFiles)
    assert log_size == len(file_manager.loadLogNames())
    assert file_manager.logFiles == file_manager.loadLogNames()


def test_load_model(create_file_manager, create_graph_model, graph_model_name, vertex_list, edge_list):
    file_manager = create_file_manager
    graph_model = create_graph_model
    file_manager.saveModel(graph_model)
    final_vertex_list, final_edge_list = file_manager.loadModel(graph_model_name)
    count_vertex = 0
    count_edge = 0
    for v in vertex_list:
        for v1 in final_vertex_list:
            if v == v1:
                count_vertex += 1
    for e in edge_list:
        for e1 in final_edge_list:
            if e == e1:
                count_edge += 1
                
    assert count_vertex == len(vertex_list)
    assert count_edge == len(edge_list)
    file_manager.deleteFolder(graph_model_name)
    

def test_load_log(create_file_manager, create_log_model, log_model_name, tmp_log):
    file_manager = create_file_manager
    log_model = create_log_model
    file_manager.saveLog(log_model, log_model_name)
    log, meta_dict = file_manager.loadLog(log_model_name)
    assert log == tmp_log
    file_manager.deleteFolder(log_model_name)
    
    