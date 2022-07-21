import os

from utilities.FileManager import FileManager

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

tool_bar_skeleton = """
MDToolbar:
    title: "Menu"
"""


class DefaultScreen:
    def __init__(self, graph_controller):
        self.graph_box_color = [41 / 255, 162 / 255, 162 / 255, 1]
        self.log_box_color = [41 / 255, 162 / 255, 162 / 255, 1]

        self.graph_box_color_1 = [153 / 255, 157 / 255, 157 / 255, 1]
        self.log_box_color_1 = [153 / 255, 157 / 255, 157 / 255, 1]

        self.fm = FileManager(os.getcwd() + "/data/")

        self.graph_controller = graph_controller

    def build_screen(self):
        # create the graph list
        layout = GridLayout(cols=1,
                            row_force_default=True,
                            row_default_height='50dp',
                            size_hint_y=None,
                            spacing=[30, 10],
                            padding=[20, 0, 20, 50])
        # necessary for scolling
        layout.bind(minimum_height=layout.setter('height'))

        flip = True
        if self.fm.graphFolders:
            #layout.add_widget(self.build_graph_box_layout(self.fm.graphFolders[0], self.graph_box_color))
            modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp",
                                   md_bg_color=self.log_box_color,
                                   radius=[10])
            modelBox.add_widget(MDLabel(text="Graphs:"))
            layout.add_widget(modelBox)

        for model in self.fm.graphFolders:
            if flip:
                layout.add_widget(self.build_graph_box_layout(model, self.graph_box_color))
                flip = False
            else:
                layout.add_widget(self.build_graph_box_layout(model, self.graph_box_color_1))
                flip = True

        # create the log list
        layout1 = GridLayout(cols=1,
                             row_force_default=True,
                             row_default_height='50dp',
                             size_hint_y=None,
                             spacing=[30, 10],
                             padding=[20, 0, 20, 50])
        # necessary for scolling
        layout1.bind(minimum_height=layout1.setter('height'))

        flip = True
        # else the first element is not displayed
        if self.fm.logFolders:
            #layout1.add_widget(self.build_log_box_layout(self.fm.logFolders[0], self.log_box_color))
            modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=self.log_box_color,
                                   radius=[10])
            modelBox.add_widget(MDLabel(text="Logs:"))
            layout1.add_widget(modelBox)

        for log in self.fm.logFolders:
            if flip:
                layout1.add_widget(self.build_log_box_layout(log, self.log_box_color))
                flip = False
            else:
                layout1.add_widget(self.build_log_box_layout(log, self.log_box_color_1))
                flip = True

        # a grid that holds two grids
        topGrid = GridLayout(cols=2,
                             row_force_default=True,
                             row_default_height='40dp',
                             size_hint_y=None,
                             spacing=[30, 10],
                             padding=[0, 0, 0, 20])
        # make the graph list scrollable
        scroll = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), scroll_type=["bars"])
        scroll.add_widget(layout)
        topGrid.add_widget(scroll)

        # make the log list scrollable
        scroll1 = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), scroll_type=["bars"])
        scroll1.add_widget(layout1)
        topGrid.add_widget(scroll1)

        tool1 = Builder.load_string(tool_bar_skeleton)

        create_button = Button(text="create model", background_color=self.graph_box_color_1)
        create_button.bind(on_press=lambda instance: self.graph_controller.create_model())

        simulation_overview_button = Button(text="simulation overview", background_color=self.graph_box_color_1)
        simulation_overview_button.bind(on_press=lambda instance: self.graph_controller.simulation_overview())

        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", radius=[10])
        modelBox.add_widget(create_button)
        #modelBox.add_widget(simulation_overview_button)

        tool1.add_widget(modelBox)
        # combine both element two one screen
        screen = Screen()
        screen.add_widget(tool1)
        screen.add_widget(topGrid)

        return screen

    def build_graph_box_layout(self, modelName, color):
        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=color, radius=[10])
        btn1 = MDLabel(text=modelName)
        btn2 = Button(text='edit')
        btn2.bind(on_press=lambda instance: self.graph_controller.edit_model(modelName))
        btn3 = Button(text='view')
        btn3.bind(on_press=lambda instance: self.graph_controller.view_model(modelName))
        btn4 = Button(text='simulate')
        btn4.bind(on_press=lambda instance: self.graph_controller.simulate_model(modelName))
        btn5 = Button(text='collaborate')
        btn5.bind(on_press=lambda instance: self.graph_controller.collaborate_model(modelName))

        modelBox.add_widget(btn1)
        modelBox.add_widget(btn2)
        modelBox.add_widget(btn3)
        modelBox.add_widget(btn4)
        modelBox.add_widget(btn5)

        return modelBox

    def build_log_box_layout(self, logName, color):
        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=color, radius=[10])
        btn1 = MDLabel(text=logName)
        btn2 = Button(text='view')
        btn2.bind(on_press=lambda instance: self.graph_controller.view_log(logName))
        btn3 = Button(text='model')
        btn3.bind(on_press=lambda instance: self.graph_controller.model_log(logName))
        btn4 = Button(text='share')
        btn4.bind(on_press=lambda instance: self.graph_controller.share_log(logName))

        modelBox.add_widget(btn1)
        modelBox.add_widget(btn2)
        modelBox.add_widget(btn3)
        modelBox.add_widget(btn4)

        return modelBox
