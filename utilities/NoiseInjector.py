class NoiseInjector:
    """
    A tool to inject noise into a generated log.
    """

    def __init__(self, logSize, noiseAmount, noiseDistribution, log, graph):
        self.logSize = logSize
        self.noiseAmount = noiseAmount
        self.noiseDistribution = noiseDistribution
        self.log = log
        self.graph = graph

    def injectNoise(self):
        import random
        import math
        # noise in percent (0-100) as decimal to 0.0-1.0
        self.noiseAmount /= 100
        numOfTraces = int(self.noiseAmount * self.logSize)

        # get traces to inject noise into
        index_traces_to_inject = random.choices(range(0, self.logSize), k=numOfTraces)

        traces_to_inject = []
        for index in index_traces_to_inject:
            traces_to_inject.append(self.log[index])

        tmp_log = self.log.copy()

        tmp_injections = self.noiseDistribution[0] / 100
        if math.floor(tmp_injections) == math.ceil(tmp_injections):
            injections = int(tmp_injections * numOfTraces)
        else:
            injections = int(math.ceil(tmp_injections * numOfTraces))

        tmp_deletions = self.noiseDistribution[1] / 100
        if math.floor(tmp_deletions) == math.ceil(tmp_deletions):
            deletions = int(tmp_deletions * numOfTraces)
        else:
            deletions = int(math.ceil(tmp_deletions * numOfTraces))

        tmp_modifications = self.noiseDistribution[2] / 100
        if math.floor(tmp_modifications) == math.ceil(tmp_modifications):
            modifications = int(tmp_modifications * numOfTraces)
        else:
            modifications = int(round(tmp_modifications * numOfTraces))

        range_injection = range(0, injections)
        range_deletions = range(injections, injections + deletions)
        range_modifications = range(injections + deletions, injections + deletions + modifications)

        # prevents a one of error
        if injections + deletions + modifications != len(traces_to_inject):
            range_modifications = range(injections + deletions, len(traces_to_inject))

        all_vertices = self.graph.getVertexNames()
        noised_traces = []

        for i in range_injection:
            tmp_trace = traces_to_inject[i]
            # select vertex to inject
            vertex_name = random.choices(all_vertices)[0]
            index = random.randint(0, len(tmp_trace) - 1)
            tmp_trace.insert(index, vertex_name)
            noised_traces.append(tmp_trace)

        for i in range_deletions:
            tmp_trace = traces_to_inject[i]
            index = random.randint(0, len(tmp_trace) - 1)
            del tmp_trace[index]
            noised_traces.append(tmp_trace)

        for i in range_modifications:
            tmp_trace = traces_to_inject[i]
            index_1 = random.randint(0, len(tmp_trace) - 1)
            index_2 = random.randint(0, len(tmp_trace) - 1)

            tmp_trace[index_2], tmp_trace[index_1] = tmp_trace[index_1], tmp_trace[index_2]
            noised_traces.append(tmp_trace)

        # inject noised traces into the log
        for i in range(0, len(index_traces_to_inject)):
            tmp_log[index_traces_to_inject[i]] = noised_traces[i]

        return tmp_log
