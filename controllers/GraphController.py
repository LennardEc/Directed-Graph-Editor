import os

from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

import unicodedata
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from models.GraphModel import GraphModel
from utilities.FileManager import FileManager
from utilities.GraphModelChecker import GraphModelChecker
from views.graph.GraphEditor import GraphEditor

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


class GraphController(Screen):
    """
    The `GraphController` class represents a controller implementation.
    Coordinates work of the view with the model.

    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def initialize_model(self, value):
        """
        The function is called to initiate an empty model or load an existing model from disk
        """
        if value in self.fm.graphFolders:
            vl, el = self.fm.loadModel(value)
            self.model = GraphModel(value, vl, el)
        else:
            self.model = GraphModel(value)

    def get_visualized_graph(self):
        """
        create a picture and return a kivy image
        """
        png = self.model.visualise()
        image = Image(source=png, size_hint=(None, None))
        os.remove(png)
        return image

    def update_picture(self):
        png = self.model.visualise()
        self.image.source = png
        self.image.reload()
        os.remove(png)

    # model callback functions
    def add_vertex(self, name, source, sink):
        if self.model.validateVertex(name):
            dia = MDDialog(title="Vertex alreay exist!")
            dia.open()
        else:
            self.model.addVertex(name, source, sink)
            self.undo.append(("delete_vertex", self.model.deleteVertex, name, source, sink))
            self.update_picture()

    def add_edge(self, start, end, weight):
        if is_number(weight) or weight == "" or weight == "weight":
            if weight == "" or weight == "weight":
                weight = 1.0
            else:
                weight = float(weight)
        else:
            dia = MDDialog(title="Invalid weight!")
            dia.open()

        if self.model.validateEdge(start, end, weight):
            self.model.addEdge(start, end, weight)
            self.undo.append(("delete_edge", self.model.deleteEdge, start, end, weight))
            self.update_picture()
        else:
            dia = MDDialog(title="Invalid edge!")
            dia.open()

    def edit_vertex(self, name, source, sink, delete):
        if self.model.validateVertex(name):
            if delete:
                self.model.deleteVertex(name)
                tmp_vertex = self.model.getVertex(name)
                self.undo.append(("add_vertex", self.model.addVertex, name, tmp_vertex.source, tmp_vertex.sink))
                self.update_picture()
            else:
                if source:
                    self.model.vertexChangeSource(name, True)
                    self.undo.append(("change_source", self.model.vertexChangeSource, name, False))
                elif not source:
                    self.model.vertexChangeSource(name, False)
                    self.undo.append(("change_source", self.model.vertexChangeSource, name, True))

                if sink:
                    self.model.vertexChangeSink(name, True)
                    self.undo.append(("change_sink", self.model.vertexChangeSink, name, False))
                elif not sink:
                    self.model.vertexChangeSink(name, False)
                    self.undo.append(("change_sink", self.model.vertexChangeSink, name, True))
        else:
            dia = MDDialog(title="Vertex does not exist!")
            dia.open()

    def change_name(self, name, new_name):
        if self.model.validateVertex(name):
            if not self.model.validateVertex(new_name):
                self.model.modifyVertexName(name, new_name)
                self.undo.append(("change_name", self.model.modifyVertexName, new_name, name))
                self.update_picture()
        else:
            dia = MDDialog(title="Vertex does not exist!")
            dia.open()

    def edit_edge(self, start, end, weight, delete):
        if delete:
            self.model.deleteEdge(start, end)
            self.undo.append(("add_edge", self.model.addEdge, start, end, weight))
            self.update_picture()
        else:
            if self.model.isEdge(start, end):
                if is_number(weight) or weight == "" or weight == "weight":
                    if weight == "" or weight == "weight":
                        weight = 1.0
                    else:
                        weight = float(weight)
                        if weight > 0.0:
                            self.model.modifyEdge(start, end, weight)
                            self.update_picture()
                        else:
                            dia = MDDialog(title="Invalid weight!")
                            dia.open()
                else:
                    dia = MDDialog(title="Invalid weight!")
                    dia.open()
            else:
                dia = MDDialog(title="Edge does not exist! ")
                dia.open()

    def __init__(self, **kw):
        """
        The constructor takes a reference to the model.
        The constructor creates the view.
        """
        super().__init__(**kw)
        # values
        self.model = None
        self.screen_manager = None
        self.screens = None

        self.image = None

        self.undo = []
        self.redo = []

        self.fm = FileManager(os.getcwd() + "/data/")

        self.current_screen_build = self.build_screen
        self.add_widget(self.current_screen_build)

    @property
    def build_screen(self):
        ge = GraphEditor(self)
        return ge.build_screen()

    def undo_action(self):
        if self.undo:
            todo = self.undo.pop()
            self.redo.append(todo)

            if todo[0] == "delete_vertex":
                todo[1](todo[2])
                self.update_picture()
            elif todo[0] == "add_vertex":
                todo[1](todo[2])
                self.update_picture()
            elif todo[0] == "delete_edge":
                todo[1](todo[2], todo[3])
                self.update_picture()
            elif todo[0] == "add_edge":
                todo[1](todo[2], todo[3], todo[4])
                self.update_picture()
            elif todo[0] == "change_source":
                todo[1](todo[2], todo[3])
                self.update_picture()
            elif todo[0] == "change_sink":
                todo[1](todo[2], todo[3])
                self.update_picture()
            elif todo[0] == "change_name":
                todo[1](todo[2], todo[3])
                self.update_picture()
            else:
                print()

    def redo_action(self):
        if self.redo:
            todo = self.redo.pop()
            self.undo.append(todo)

            if todo[0] == "delete_vertex":
                self.model.addVertex(todo[2], todo[3], todo[4])
                self.update_picture()
            elif todo[0] == "add_vertex":
                self.model.deleteVertex(todo[2], todo[3], todo[4])
                self.update_picture()
            elif todo[0] == "delete_edge":
                self.model.addEdge(todo[2], todo[3])
                self.update_picture()
            elif todo[0] == "add_edge":
                self.model.deleteEdge(todo[2], todo[3])
                self.update_picture()
            elif todo[0] == "change_source":
                self.model.vertexChangeSource(todo[2], not todo[3])
                self.update_picture()
            elif todo[0] == "change_sink":
                self.model.vertexChangeSink(todo[2], not todo[3])
                self.update_picture()
            elif todo[0] == "change_name":
                todo[1](todo[3], todo[2])
                self.update_picture()
            else:
                print()

    def back_to_menu(self):
        accept = MDRaisedButton(text="accept")
        dia = MDDialog(title="All changes will be discarded!", buttons=[accept])
        accept.bind(on_press=lambda x: self._close(dia))
        dia.open()

    def _close(self, dia):
        dia.dismiss(force=True)
        self.undo = []
        self.redo = []
        self.screen_manager.switch_to(self.screens[0])

    def save_model(self):
        checker = GraphModelChecker(self.model)
        res = checker.is_legal_graph()

        if res == True:
            self.fm.saveModel(self.model)
            self.screen_manager.switch_to(self.screens[0])
        else:
            string = "Unexpceted error"
            if res[1] == "not_connected":
                string = "The following sources are not connected to sinks: \n" + str(res[2])

            if res[1] == "deadlocks":
                string = "The following nodes/vertices are deadlocks (a vertex that is not a sink without any edges): \n" + str(res[2])

            dia = MDDialog(title=string)
            dia.open()

    def on_pre_enter(self, *args):
        self.remove_widget(self.current_screen_build)
        self.current_screen_build = self.build_screen
        self.add_widget(self.current_screen_build)

    def set_parameters(self, screen_manager, screens):
        self.screen_manager = screen_manager
        self.screens = screens
