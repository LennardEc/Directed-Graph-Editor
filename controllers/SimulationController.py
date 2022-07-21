import os
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from kivy.clock import Clock
from kivymd.uix.progressbar import MDProgressBar

from models.GraphModel import GraphModel
from models.SimulationModel import SimulationModel

from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.uix.screenmanager import Screen
from utilities.FileManager import FileManager
from utilities.GraphModelChecker import GraphModelChecker
from views.simulation.SimulationView import SimulationView

"""
    def front(): void
    def start(graph) : void 
    def createSimulation(SimulationModel) : void
    def viewOngoingSimulation(simulation)
    def viewAllOngoingSimulation()
    def _refreshProgress()
    def cancel(futureObject)
"""


class SimulationController(Screen):
    """
    The `SimulationController` class represents a controller implementation.
    Coordinates work of the view with the model.

    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def initialize_model(self, value):
        """
        The function is called to initiate an empty model or load an existing model from disk
        """
        vl, el = self.fm.loadModel(value)
        self.model = GraphModel(value, vl, el)

    def set_parameters(self, screen_manager, screens, simulation_manager):
        self.screen_manager = screen_manager
        self.screens = screens
        self.simulation_manager = simulation_manager

    def __init__(self, **kw):
        super().__init__(**kw)

        self.label = None
        self.progress_bar = None
        self.process_bar_popup = None
        self.model = None
        self.screen_manager = None
        self.screens = None
        self.parameters = None
        self.simulation_manager = None

        self.executor = ProcessPoolExecutor()
        self.fm = FileManager(os.getcwd() + "/data/")

        self.current_screen = self.build_screen

        self.add_widget(self.current_screen)

    @property
    def build_screen(self):
        sv = SimulationView(self)
        return sv.build_screen()

    def on_pre_enter(self, *args):
        # update the screen with the new model
        self.remove_widget(self.current_screen)
        self.current_screen = self.build_screen
        self.add_widget(self.current_screen)

        # check if the model is legal
        self.legal_model()

    def legal_model(self):
        checker = GraphModelChecker(self.model)
        res = checker.is_legal_graph()
        try:
            if res[0] == False:
                if res[1] == "Graph misses either a source or sink":
                    string = "Graph misses either a source or sink"
                    text = ""

                if res[1] == "not_connected":
                    string = "The following sources are not connected to sinks:"
                    text = str(res[2])

                if res[1] == "deadlocks":
                    string = "The following nodes/vertices are deadlocks (a vertex that is not a sink without any edges):"
                    text = str(res[2])

                go_to_editor = MDRaisedButton(text="go to editor")
                back_to_menu = MDRaisedButton(text="home")

                go_to_editor.bind(on_press=lambda x: [dia.dismiss(force=True),
                                                      self.screens[4].initialize_model(self.model.name),
                                                      self.screen_manager.switch_to(self.screens[4])])

                back_to_menu.bind(on_press=lambda x: [dia.dismiss(force=True),
                                                      self.screen_manager.switch_to(self.screens[0])])

                dia = MDDialog(title=string, text=text, buttons=[go_to_editor, back_to_menu])
                dia.open()
        except:
            pass

    def back_to_menu(self):
        self.screen_manager.switch_to(self.screens[0])

    def start_simulation_button(self):
        if self.validate_parameters(self.parameters):
            self.start_simulation(self.model,
                                  int(self.parameters["Number of traces"].text),
                                  int(self.parameters["Minimal trace length"].text),
                                  int(self.parameters["Maximal trace length"].text),
                                  int(self.parameters["Noise in percentage"].text),
                                  (float(self.parameters["Amount of insertion"].text),
                                   float(self.parameters["Amount of deletion"].text),
                                   float(self.parameters["Amount of modification"].text))
                                  )

    def validate_parameters(self, parameters):
        try:
            if not (int(parameters["Number of traces"].text) > 1):
                return False

            if not (1 <= int(parameters["Minimal trace length"].text) <= int(parameters["Maximal trace length"].text)):
                return False

            if not (0.0 <= int(parameters["Noise in percentage"].text) <= 100.0):
                return False

            if not (float(parameters["Amount of insertion"].text) +
                    float(parameters["Amount of deletion"].text) +
                    float(parameters["Amount of modification"].text) == 100.0):
                return False

            return True
        except:
            return False

    # called by the start_simulation_action function
    def start_simulation(self, graph, logSize, minTrace, maxTrace, noiseAmount, noiseDistribution):
        # todo create a name
        simulation_name = graph.name + " log " + str(random.randint(0, 100)) + " - " + str(random.randint(0, 100))

        simulation = SimulationModel(graph, logSize, minTrace, maxTrace, noiseAmount, noiseDistribution, simulation_name)
        future = self.executor.submit(simulation.simulation)

        # add simulation and future to simulation manager
        self.simulation_manager.ongoingSimulations.append(simulation)
        self.simulation_manager.futures.append(future)
        self.simulation_manager.mapping[simulation_name] = (simulation, future)

        #call the progress bar
        self.show_process_bar(simulation)

    def _update_dialog_string(self, simulation):
        progress = self.fm.getProgress(simulation.name)
        percentage = (progress[0] / simulation.logSize) * 100
        text_string = "Total tries: " + str(sum(progress)) + "\n" + \
                      "Traces: " + str(progress[0]) + "/" + str(simulation.logSize) + "\n" + \
                      "Max Trace length exceeded: " + str(progress[2])

        # "Occurred Deadlocks: " + str(progress[1]) + "\n" + \

        self.progress_bar.value = percentage
        self.label.text = text_string
        
    def show_process_bar(self, simulation):
        title_string = "Simulation Status: " + str(simulation.name)

        box = MDBoxLayout(orientation="vertical", padding=[20, 20, 20, 20])

        self.progress_bar = MDProgressBar()
        self.label = MDLabel(text="")

        box.add_widget(self.progress_bar)
        box.add_widget(self.label)
        
        cancel_button = MDRaisedButton(text="Cancel")
        cancel_button.bind(on_press=lambda x: [self.cancel_simulation(simulation.name), self.process_bar_popup.dismiss(force=True), event.cancel()])
        
        close_button = MDRaisedButton(text="Close")
        close_button.bind(on_press=lambda x: [self.process_bar_popup.dismiss(force=True), event.cancel()])

        self.process_bar_popup = MDDialog(title=title_string, buttons=[cancel_button, close_button], height="200dp")
        self.process_bar_popup.add_widget(box)
        self._update_dialog_string(simulation)
        self.process_bar_popup.open()

        event = Clock.schedule_interval(lambda x: self._update_dialog_string(simulation), 1)
        #event.cancel()
        
    # todo not just flag
    def cancel_simulation(self, simulation_name):
        self.simulation_manager.cancel_ongoing_simulation(simulation_name)

    def cancel_ongoing_simulation(self, simulation):
        simulation.cancel()
        self.simulation_manager.ongoingSimulations.remove(simulation)