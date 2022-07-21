import os

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

from models.GraphModel import GraphModel
from utilities.FileManager import FileManager
from utilities.ResizableDraggablePicture import ResizableDraggablePicture

tool_bar_skeleton = """
MDToolbar:
    title: "Model View"
"""


class ViewGraphController(Screen):
    """
    Presents the visuals of a model
    """

    def initialize_model(self, value):
        """
        The function is called to initiate an empty model or load an existing model from disk
        """
        vl, el = self.fm.loadModel(value)
        self.model = GraphModel(value, vl, el)

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

    def to_editor(self):
        editor = self.screens[4]
        editor.initialize_model(self.model.name)
        self.screen_manager.switch_to(editor)

    def on_pre_enter(self, *args):
        self.remove_widget(self.current_screen_build)
        self.current_screen_build = self.build_screen
        self.add_widget(self.current_screen_build)

    def get_visualized_graph(self):
        """
        create a picture and return a kivy image
        """
        png = self.model.visualise()
        image = Image(source=png,
                      size_hint=(None, None),
                      keep_ratio=True,
                      size=Window.size)
        os.remove(png)
        return image

    @property
    def build_screen(self):
        layout = MDBoxLayout(orientation='vertical', radius=[10])
        scatter = ResizableDraggablePicture(do_rotation=False, do_scale=True)

        if self.model is not None:
            image = self.get_visualized_graph()
        else:
            # todo remove place holder
            image = Image(source="placeholder.png")

        scatter.add_widget(image)
        layout.add_widget(scatter)

        tool1 = Builder.load_string(tool_bar_skeleton)

        create_button = Button(text="back to menu", background_color=self.graph_box_color_1)
        create_button.bind(on_press=lambda instance: self.back_to_menu())

        simulation_overview_button = Button(text="go to editor", background_color=self.graph_box_color_1)
        simulation_overview_button.bind(on_press=lambda instance: self.to_editor())

        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", radius=[10])
        modelBox.add_widget(create_button)
        modelBox.add_widget(simulation_overview_button)

        tool1.add_widget(modelBox)

        screen = Screen()
        screen.add_widget(layout)
        screen.add_widget(tool1)

        return screen
