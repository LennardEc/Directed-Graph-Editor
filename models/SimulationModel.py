import os
from datetime import date

from models.LogModel import LogModel
from utilities.FileManager import FileManager
from utilities.NoiseInjector import NoiseInjector
from utilities.ProcessEngine import ProcessEngine
from utilities.CostumExceptions import DeadLock
from utilities.CostumExceptions import TraceLengthExceeded


class SimulationModel:
    """
    The SimulationModel class is a data model implementation.

    The model is (primarily) responsible for the logic of the application.
    """

    def __init__(self, graph, logSize, minTrace, maxTrace, noiseAmount, noiseDistribution, name):
        self.graph = graph
        self.logSize = logSize
        self.minTrace = minTrace
        self.maxTrace = maxTrace
        self.processEngine = ProcessEngine(self.graph, self.minTrace, self.maxTrace)
        self.noiseAmount = noiseAmount
        self.noiseDistribution = noiseDistribution
        self.log = []
        self.done = False
        self.progress_stats = [0, 0, 0] #number of traces, dead logs, trace length succeed
        self.fm = FileManager(os.getcwd() + "/data/")
        self.name = name

    def simulation(self):
        self.simulate()

        if self.noiseAmount != 0.0:
            noise = NoiseInjector(self.logSize,
                                  self.noiseAmount,
                                  self.noiseDistribution,
                                  self.log,
                                  self.graph)
            self.log = noise.injectNoise()

        # todo remove in final version
        print("simulation finished")

        self.done = True

        logModel = LogModel(self.name,
                            self.log,
                            self.graph.name,
                            self.logSize,
                            self.noiseAmount,
                            self.noiseDistribution,
                            date.today())
        self.fm.saveLog(logModel, self.name)

        return self.name

    def toString(self):
        return self.name

    def progress(self):
        return self.progress_stats

    def simulate(self):
        log = []
        counter = 0
        # initialize file
        self.fm.writeProgress(self.name, self.progress_stats)

        # todo make file write
        while len(log) < self.logSize:
            if counter % (self.logSize/10) == 0:
                self.fm.writeProgress(self.name, self.progress_stats)

            try:
                curr_trace = self.processEngine.generateTrace()
                log.append(curr_trace)
                self.progress_stats[0] += 1
            except DeadLock:
                self.progress_stats[1] += 1
            except TraceLengthExceeded:
                self.progress_stats[2] += 1
            counter += 1
        self.fm.writeProgress(self.name, self.progress_stats)
        self.log = log
