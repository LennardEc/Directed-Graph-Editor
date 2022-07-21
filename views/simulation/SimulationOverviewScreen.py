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
    title: "Simulation Overview"
"""


class SimulationOverviewScreen:
    def __init__(self, simulation_overview_controller):
        self.simulation_overview_controller = simulation_overview_controller

        self.graph_box_color = [41 / 255, 162 / 255, 162 / 255, 1]
        self.log_box_color = [41 / 255, 162 / 255, 162 / 255, 1]

        self.graph_box_color_1 = [153 / 255, 157 / 255, 157 / 255, 1]
        self.log_box_color_1 = [153 / 255, 157 / 255, 157 / 255, 1]

    def build_simulation_layout(self, name, color):
        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=color, radius=[10])
        btn1 = MDLabel(text=name)

        modelBox.add_widget(btn1)
        return modelBox

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

        running = []
        finished = []

        # print(self.simulation_manager.view_futures())
        # print(self.simulation_manager.view_futures()[0].done())

        for fut in self.simulation_overview_controller.simulation_manager.view_futures():
            if fut.done():
                finished.append(fut)
            else:
                running.append(fut)

        flip = True
        # Todo fix
        # else the first element is not displayed
        if running:
            layout.add_widget(self.simulation_overview_controller.build_simulation_layout(running[0].result(), self.graph_box_color))

        for run in running:
            if flip:
                layout.add_widget(self.simulation_overview_controller.build_simulation_layout(run.result(), self.graph_box_color))
                flip = False
            else:
                layout.add_widget(self.simulation_overview_controller.build_simulation_layout(run.result(), self.graph_box_color_1))
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
        if finished:
            layout1.add_widget(self.simulation_overview_controller.build_simulation_layout(finished[0].result(), self.log_box_color))

        for fin in finished:
            if flip:
                layout1.add_widget(self.simulation_overview_controller.build_simulation_layout(fin.result(), self.log_box_color))
                flip = False
            else:
                layout1.add_widget(self.simulation_overview_controller.build_simulation_layout(fin.result(), self.log_box_color_1))
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

        back_to_menu_button = Button(text="back to menu", background_color=self.graph_box_color_1)
        back_to_menu_button.bind(on_press=lambda instance: self.simulation_overview_controller.back_to_menu())

        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", radius=[10])
        modelBox.add_widget(back_to_menu_button)

        tool1.add_widget(modelBox)
        # combine both element two one screen
        screen = Screen()
        screen.add_widget(tool1)
        screen.add_widget(topGrid)

        return screen

    def build_empty_screen(self):
        layout = GridLayout(cols=1,
                            row_force_default=True,
                            row_default_height='50dp',
                            size_hint_y=None,
                            spacing=[30, 10],
                            padding=[20, 0, 20, 50])
        # necessary for scolling
        layout.bind(minimum_height=layout.setter('height'))

        # create the log list
        layout1 = GridLayout(cols=1,
                             row_force_default=True,
                             row_default_height='50dp',
                             size_hint_y=None,
                             spacing=[30, 10],
                             padding=[20, 0, 20, 50])
        # necessary for scolling
        layout1.bind(minimum_height=layout1.setter('height'))

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

        back_to_menu_button = Button(text="back to menu", background_color=self.graph_box_color_1)
        back_to_menu_button.bind(on_press=lambda instance: self.simulation_overview_controller.back_to_menu())

        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", radius=[10])
        modelBox.add_widget(back_to_menu_button)

        tool1.add_widget(modelBox)
        # combine both element two one screen
        screen = Screen()
        screen.add_widget(tool1)
        screen.add_widget(topGrid)

        return screen