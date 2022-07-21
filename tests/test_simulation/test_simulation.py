import pytest
from models.SimulationModel import SimulationModel
from models.GraphModel import GraphModel
from models.VertexModel import VertexModel
from models.EdgeModel import EdgeModel
import random
import string

@pytest.fixture(scope="module")
def graph():
    vertexList =  [VertexModel("A", True), VertexModel("B"), VertexModel("C", False, True)]
    edgeList = [EdgeModel("A", "B"), EdgeModel("B", "C")]
    graph_model = GraphModel("Graph1", vertexList, edgeList)
    yield graph_model

@pytest.fixture(scope="module")
def graph_with_one_node():
    vertexList =  [VertexModel("A", True, True)]
    edgeList = [EdgeModel("A", "A")]
    graph_model = GraphModel("Graph2", vertexList, edgeList)
    yield graph_model

@pytest.fixture(scope="module")
def graph_with_num_node():
    num = 600
    vertexList = [VertexModel("A", True)]
    edgeList = []
    vertexNameLatest = "A"
    for i in range(num):
        vertexName = id_generator()
        vertexList.append(VertexModel(vertexName, True))
        edgeList.append(EdgeModel(vertexNameLatest, vertexName))
        vertexNameLatest = vertexName
    vertexList[num-1] = VertexModel(vertexList[num-1].name, False, True)
    graph_model = GraphModel("Graph100", vertexList, edgeList)
    yield graph_model

@pytest.fixture(scope="module")
def log_size():
    logSize = 1000
    yield logSize

@pytest.fixture(scope="module")
def min_trace():
    minTrace = 1
    yield minTrace

@pytest.fixture(scope="module")
def max_trace():
    maxTrace = 100
    yield maxTrace

@pytest.fixture(scope="module")
def noise_amount():
    noiseAmount = 10
    yield noiseAmount

@pytest.fixture(scope="module")
def noise_distribution():
    noiseDistribution = (50,25,25)
    yield noiseDistribution

@pytest.fixture(scope='function')
def create_simulation(graph, log_size, min_trace, max_trace, noise_amount, noise_distribution):
    name = graph.name + " log " + "1"
    simulation_model = SimulationModel(graph, log_size, min_trace, max_trace, noise_amount, noise_distribution, name)
    yield simulation_model

@pytest.fixture(scope='function')
def create_simulation_one_node(graph_with_one_node, log_size, noise_distribution):
    name = graph_with_one_node.name + " log " + "1"
    simulation_model = SimulationModel(graph_with_one_node, log_size, 1, 1, 0, noise_distribution, name)
    yield simulation_model

@pytest.fixture(scope='function')
def create_simulation_num(graph_with_num_node, log_size, min_trace, noise_amount, noise_distribution):
    name = graph_with_num_node.name + " log " + "1"
    simulation_model = SimulationModel(graph_with_num_node, log_size, min_trace, 10000, noise_amount, noise_distribution, name)
    yield simulation_model

def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def test_simulate(create_simulation, create_simulation_one_node):
    simulation_model = create_simulation
    simulation_model.simulate()
    simulation_model_one_node = create_simulation_one_node
    simulation_model_one_node.simulate()
    assert len(simulation_model.log) == simulation_model.logSize
    assert len(simulation_model_one_node.log) == simulation_model_one_node.logSize

def test_simulation(create_simulation):
    simulation_model = create_simulation
    log_name = simulation_model.simulation()
    assert log_name == simulation_model.name

def test_simulation_num(create_simulation_num):
    simulation_model = create_simulation_num
    log_name = simulation_model.simulation()
    assert log_name == simulation_model.name