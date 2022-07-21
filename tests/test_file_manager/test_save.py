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
    

def test_prep(create_file_manager, graph_model_name, log_model_name):
    file_manager = create_file_manager
    folder_value_graph = file_manager.existsFolder(graph_model_name)
    assert False == folder_value_graph
    file_value_graph  = file_manager.existsFile(graph_model_name + ".txt")
    assert False == file_value_graph
    
    folder_value_log = file_manager.existsFolder(log_model_name)
    assert False == folder_value_log
    file_value_log  = file_manager.existsFile(log_model_name + ".xes")
    assert False == file_value_log
    
    meta_value_log = file_manager.existsFile("meta_" + log_model_name + ".txt")
    assert False == meta_value_log
    

def test_create_graph_model(create_graph_model, graph_model_name):
    graph_model = create_graph_model
    assert 3 == len(graph_model.vertexDict)
    
def test_save_model(create_file_manager, create_graph_model, graph_model_name):
    file_manager = create_file_manager
    graph_model = create_graph_model
    file_manager.saveModel(graph_model)
    folder_value = file_manager.existsFolder(graph_model_name)
    assert True == folder_value
    file_value = file_manager.existsFile(graph_model_name + ".txt")
    assert True == file_value 
    file_manager.deleteFolder(graph_model_name)

def test_save_log(create_file_manager, create_log_model, log_model_name):
    file_manager = create_file_manager
    log_model = create_log_model
    file_manager.saveLog(log_model, log_model_name)
    file_value = file_manager.existsFile(log_model_name + ".xes")
    assert True == file_value
    meta_value = file_manager.existsFile("meta_" + log_model_name + ".txt")
    assert True == meta_value
    file_manager.deleteFolder(log_model_name)
    
    
    
