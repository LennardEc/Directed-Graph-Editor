class LogModel:
    """
    The LogModel class is a data model implementation. 

    The model is (primarily) responsible for the logic of the application.
    """

    def __init__(self, name, log, modelName, logSize, noiseInPercent, distributionOfNoise, timeOfCreation):
        self.name = name
        self.log = log
        self.logSize = logSize
        self.modelName = modelName
        self.distributionOfNoise = distributionOfNoise
        self.noiseInPercent = noiseInPercent
        self.timeOfCreation = timeOfCreation
    
    def toString(self):
        """
        returns the meta data as a string
        """
        return "name:" + self.name + "\n" +\
               "name of the model:" + self.modelName + "\n" +\
               "time of creation:" + str(self.timeOfCreation) + "\n" + \
               "log size:" + str(self.logSize) + "\n" + \
               "amount of noise:" + str(self.noiseInPercent) + "\n" +\
               "distribution:" + str(self.distributionOfNoise) + "\n" +\
               "time of creation:" + str(self.timeOfCreation)
