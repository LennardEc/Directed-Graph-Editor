import os

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from models.LogModel import LogModel
from utilities.FileManager import FileManager

tool_bar_skeleton = """
MDToolbar:
    title: "Model View"
"""


class ViewLogController(Screen):
    """
    Presents the visuals of a model
    """

    def initialize_model(self, value):
        """
        The function is called to initiate an empty model or load an existing model from disk
        """
        log, meta_dict = self.fm.loadLog(value)
        self.model = LogModel(value,
                              log,
                              meta_dict["name of the model"],
                              meta_dict["log size"],
                              meta_dict["amount of noise"],
                              meta_dict["distribution"],
                              meta_dict["time of creation"])

    def set_parameters(self, screen_manager, screens):
        self.screen_manager = screen_manager
        self.screens = screens

    def __init__(self, **kw):
        super().__init__(**kw)
        self.model = None
        self.current_screen = None
        self.screen_manager = None
        self.screens = None

        self.graph_box_color_1 = [153 / 255, 157 / 255, 157 / 255, 1]

        self.fm = FileManager(os.getcwd() + "/data/")

        self.current_screen_build = self.build_screen
        self.add_widget(self.current_screen_build)

    def back_to_menu(self):
        self.screen_manager.switch_to(self.screens[0])

    def on_pre_enter(self, *args):
        self.remove_widget(self.current_screen_build)
        self.current_screen_build = self.build_screen
        self.add_widget(self.current_screen_build)

    @property
    def build_screen(self):
        layout = MDBoxLayout(orientation='vertical', radius=[10])

        # todo better layout
        # name, log, modelName, logSize, noiseInPercent, distributionOfNoise, timeOfCreation
        """
        if self.model is not None:
            layout.add_widget(MDLabel(text="Log Name:           " + self.model.name))
            layout.add_widget(MDLabel(text="Time of Creation:   " + str(self.model.timeOfCreation)))
            layout.add_widget(MDLabel(text="Model Name:         " + self.model.modelName))
            layout.add_widget(MDLabel(text="Amount of Noise:    " + str(self.model.noiseInPercent)))
            layout.add_widget(MDLabel(text="   insertion:       " + str(self.model.distributionOfNoise[0])))
            layout.add_widget(MDLabel(text="   deletion:        " + str(self.model.distributionOfNoise[1])))
            layout.add_widget(MDLabel(text="   modification:    " + str(self.model.distributionOfNoise[2])))
        """

        if self.model is not None:
            string = "    Log Name:       " + self.model.name + "\n" + \
                     "    Time of Creation:        " + str(self.model.timeOfCreation) + "\n" + \
                     "    Model Name:              " + self.model.modelName + "\n\n" + \
                     "    Amount of Noise:         " + str(self.model.noiseInPercent) + "%\n" + \
                     "       insertion:            " + str(self.model.distributionOfNoise[0]) + "%\n" + \
                     "       deletion:             " + str(self.model.distributionOfNoise[1]) + "%\n" + \
                     "       modification:         " + str(self.model.distributionOfNoise[2]) + "%"
            layout.add_widget(MDLabel(text=string, font_style="H4"))

        tool1 = Builder.load_string(tool_bar_skeleton)

        create_button = Button(text="back to menu", background_color=self.graph_box_color_1)
        create_button.bind(on_press=lambda instance: self.back_to_menu())

        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", radius=[10])
        modelBox.add_widget(create_button)

        tool1.add_widget(modelBox)

        screen = Screen()
        screen.add_widget(layout)
        screen.add_widget(tool1)

        return screen
