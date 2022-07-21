"""
    class FileManager:

    def __init__(path: string)
    def loadModel(name: string) : (List<Vertex>, List<Edge>)
    def saveModel(name: string, graph: GraphModel) : void
    def loadLog(name: string) : List<string>
    def saveLog(name: string, log: LogModel) : void
    def loadModelNames() : List<string>
    def loadLogNames() : List<string>
    def existsFile(name: string) :  boolean
    def existsFolder(name: string) : boolean
    def deleteFile(name: string) : void
    def deleteFolder(name: string) : void

    def refresh() : void

    1. add and delete files when necessary
    2. fix directory
"""

import distutils.util
import os

from micropm4py.log import xes_export_traces_file
from micropm4py.log import xes_import_traces_file

from models.EdgeModel import EdgeModel
from models.VertexModel import VertexModel


class FileManager:
    def __init__(self, path):
        self.path = path

        # scan for existing folders and file
        self.graphFolders, self.graphFiles = self.scanDataFolder("graphs")
        self.logFolders, self.logFiles = self.scanDataFolder("logs")

        # work in progress todo find a better split
        self.listStart = "~~~~~~vertices~~~~~~\n"
        self.listSeparator = "~~~~~~edges~~~~~~\n"

        # create a tmp folder
        path = self.path[:-5] + "tmp"
        if not os.path.exists(path):
            os.mkdir(path)

    def refresh(self):
        self.graphFolders, self.graphFiles = self.scanDataFolder("graphs")
        self.logFolders, self.logFiles = self.scanDataFolder("logs")

    def scanDataFolder(self, subFolder):
        """
        A private function that mines the data/graphs folder for existing sub-folders and files
        """
        folderPath = self.path + subFolder + "/"
        folders = [o for o in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, o))]

        files = []
        for folder in folders:
            files += os.listdir(folderPath + folder)

        return folders, files

    def deleteFile(self, name):
        """
        deletes a file
        """
        file = name + ".txt"
        if file in self.graphFiles:
            fileLocation = self.path + "graphs/"
            isGraph = True
        else:
            fileLocation = self.path + "logs/"
            isGraph = False

        # get all directories for either graphs or logs
        directories = [o for o in os.listdir(fileLocation) if os.path.isdir(os.path.join(fileLocation, o))]

        # iterate through all files in each sub-directories
        for dirs in directories:
            if file in os.listdir(fileLocation + dirs):
                os.remove(fileLocation + dirs + "/" + file)

                # delete file from list
                if isGraph:
                    self.graphFiles.remove(file)
                else:
                    self.logFiles.remove(file)
                break

    def deleteFolder(self, folder):
        """
        deletes a folder
        """
        if folder in self.graphFolders:
            fileLocation = self.path + "graphs/"
            isGraph = True
        else:
            fileLocation = self.path + "logs/"
            isGraph = False

        # get all directories for either graphs or logs

        directories = [o for o in os.listdir(fileLocation) if os.path.isdir(os.path.join(fileLocation, o))]
        # iterate through all files in each sub-directories
        for dirs in directories:
            if folder == dirs:

                # remove all files
                for file in os.listdir(fileLocation + dirs + "/"):
                    os.remove(fileLocation + dirs + "/" + file)
                    if isGraph:
                        self.graphFiles.remove(file)
                    else:
                        self.logFiles.remove(file)
                os.rmdir(fileLocation + dirs)
                # delete folder from list
                if isGraph:
                    self.graphFolders.remove(folder)
                else:
                    self.logFolders.remove(folder)
                break

    def existsFile(self, name):
        """
        returns true if a file with the name exists
        """
        return name in (self.logFiles + self.graphFiles)

    def existsFolder(self, name):
        """
        returns true if a folder with the name exists
        """
        return name in (self.logFolders + self.graphFolders)

    def loadModelNames(self):
        """
        returns a list of all existing model files
        """
        return self.graphFiles.copy()

    def loadLogNames(self):
        """
        returns a list of all existing log files
        """
        return self.logFiles.copy()

    def saveModel(self, model):
        """
        transform a graphModel into a standardized text format
        """
        tmp_path = self.path + "graphs/"
        name = model.name

        # if folder exists over write file in folder
        # else create a new folder
        if not self.existsFolder(name):
            os.mkdir(tmp_path + name)
            self.graphFolders.append(name)

        tmp_path += name + "/"

        # retrieve all edges and vertices from the graphModel
        vertexList, edgeList = model.export()

        # build a string starting with a separator, followed by one vertex per line
        final_str = self.listStart
        for vertex in vertexList:
            final_str += vertex.name + "," + str(vertex.source) + "," + str(vertex.sink) + "\n"

        # concat the string with a separator, followed by one edge per line
        final_str += self.listSeparator
        for edge in edgeList:
            final_str += edge.start + "," + edge.end + "," + str(edge.weight) + "\n"

        # locate file and write the string
        filePath = self.path + "graphs/" + name + "/" + name + ".txt"
        file1 = open(filePath, "w")
        file1.write(final_str)
        file1.close()

        if not self.existsFile(name + ".txt"):
            self.graphFiles.append(name + ".txt")

    def loadModel(self, name):
        """
        load a text representation from a file and return a vertex and edge list
        """
        # open and read the file
        filePath = self.path + "graphs/" + name + "/" + name + ".txt"
        file = open(filePath, "r")
        lines = file.readlines()
        file.close()

        # split the list at the edge separator
        list_split = lines.index(self.listSeparator)
        # starting from one ignoring the vertex separator
        vertexList = lines[1:list_split]
        # starting from list_split + 1 to ignore the edge separator
        edgeList = lines[(list_split + 1):len(lines)]

        finalVertexList = []
        for vertex_str in vertexList:
            # remove line break
            vertex_str = vertex_str[:-1]
            vertex_values = vertex_str.split(sep=",")
            # build a vertex from the three values (name, source, sink)
            # operator.truth casts a string into a bool
            finalVertexList.append(
                VertexModel(str(vertex_values[0]),
                            bool(distutils.util.strtobool(vertex_values[1])),
                            bool(distutils.util.strtobool(vertex_values[2])))
            )

        finalEdgeList = []
        for edge_str in edgeList:
            # remove line break
            edge_str = edge_str[:-1]
            edge_values = edge_str.split(sep=",")
            # build a edge from three values (start, end, weight)
            finalEdgeList.append(
                EdgeModel(str(edge_values[0]), str(edge_values[1]), float(edge_values[2]))
            )

        return finalVertexList, finalEdgeList

    def saveLog(self, log, name):
        """
        export a log file as a xes file
        """
        tmp_path = self.path + "logs/"

        # if folder exists over write file in folder
        # else create a new folder
        if not self.existsFolder(name):
            os.mkdir(tmp_path + name)
            self.logFolders.append(name)

        tmp_path += name + "/"
        file_name = name + ".xes"
        xes_export_traces_file.export_traces(log.log, tmp_path + file_name)

        if not self.existsFile(name + ".xes"):
            self.logFiles.append(name + ".xes")

        # save the meta data of the log in the same directory
        meta_file = "meta_" + name + ".txt"
        filePath = self.path + "logs/" + name + "/" + meta_file
        file = open(filePath, "w")
        file.write(log.toString())
        file.close()

        if not self.existsFile("meta_" + name + ".txt"):
            self.logFiles.append("meta_" + name + ".txt")

    def loadLog(self, name):
        """
        import a xes file and returns a log
        """
        filePath = self.path + "logs/" + name + "/" + name + ".xes"

        log = xes_import_traces_file.imp_list_traces_from_file(filePath)

        meta_path = self.path + "logs/" + name + "/" + "meta_" + name + ".txt"
        file = open(meta_path, "r")
        meta_strings = file.readlines()
        file.close()

        meta_dict = {}
        for string in meta_strings:
            # remove line break
            tmp_str = string[:-1]

            # split string at :
            # split the list at the edge separator
            list_split = tmp_str.index(":")
            key = tmp_str[0:list_split]
            value = tmp_str[(list_split + 1):len(tmp_str)]

            meta_dict[key] = value

        # distribution needs special processing
        string = meta_dict["distribution"]
        # remove starting and end bracket
        tmp_str = string[1:-1]
        # strip string
        tmp_str = tmp_str.replace(' ', '')
        # split three values
        tmp_List = tmp_str.split(",")
        meta_dict["distribution"] = (tmp_List[0], tmp_List[1], tmp_List[2])
        return log, meta_dict

    def cleanProgress(self):
        """
        clean the tmp folder
        """
        import shutil
        path = self.path[:-5] + "tmp/"

        for x in [o for o in os.listdir(path)]:
            shutil.rmtree(path + x)

    def writeProgress(self, name, progress_stats):
        """
        saves the progress of a running simulation
        """
        # self.path[:-5] remove data/
        path = self.path[:-5] + "tmp/" + name
        if not os.path.exists(path):
            os.mkdir(path)

        path = path + "/" + name + ".txt"
        file1 = open(path, "w")
        file1.write(str(progress_stats[0]) + "," + str(progress_stats[1]) + "," + str(progress_stats[2]))
        file1.close()

    def removeProgress(self, name):
        """
        removes the data for a simulation from tmp
        """
        path = self.path[:-5] + "tmp/" + name
        try:
            os.rmdir(path)
        except:
            pass

    def getProgress(self, name):
        path = self.path[:-5] + "tmp/" + name + "/" + name + ".txt"

        try:
            file = open(path, "r")
            meta_strings = file.read()
            file.close()

            strings = meta_strings.split(",")
            return (int(strings[0]), int(strings[1]), int(strings[2]))
        except:
            return (0,0,0)
