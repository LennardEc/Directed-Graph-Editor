import os

from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox

from utilities.FileManager import FileManager
from utilities.ResizableDraggablePicture import ResizableDraggablePicture

tool_bar_skeleton = """
MDToolbar:
    title: "Editor"
"""

class GraphEditor:
    def __init__(self, graph_controller, ):
        self.graph_controller = graph_controller

        self.graph_label_color = [41 / 255, 162 / 255, 162 / 255, 1]
        self.graph_label_color_1 = [153 / 255, 157 / 255, 157 / 255, 1]

    def build_screen(self):
        layout = MDBoxLayout(orientation='vertical', radius=[10])

        parameter_form = GridLayout(cols=1,
                                    row_force_default=True,
                                    col_force_default=False,
                                    padding=[0, 0, 0, 0],
                                    row_default_height='50dp',
                                    size_hint_y=None)

        parameter_form.add_widget(self.build_add_vertex_label_layout("Add Vertex", self.graph_label_color))
        parameter_form.add_widget(self.build_edit_vertex_label_layout("Edit Vertex", self.graph_label_color))
        parameter_form.add_widget(self.build_change_name_layout("Change name", self.graph_label_color))
        parameter_form.add_widget(self.build_add_edge_label_layout("Add Edge", self.graph_label_color_1))
        parameter_form.add_widget(self.build_edit_edge_label_layout("Edit Edge", self.graph_label_color_1))

        redo_undo = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=self.graph_label_color, radius=[14])

        undo_button = Button(text="undo", background_color=self.graph_label_color_1)
        undo_button.bind(on_press=lambda inst: self.graph_controller.undo_action())
        redo_button = Button(text="redo", background_color=self.graph_label_color_1)
        redo_button.bind(on_press=lambda inst: self.graph_controller.redo_action())

        redo_undo.add_widget(undo_button)
        redo_undo.add_widget(redo_button)
        parameter_form.add_widget(redo_undo)

        layout.add_widget(parameter_form)

        # create a tool bar
        tool1 = Builder.load_string(tool_bar_skeleton)

        back_button = Button(text="back to menu", background_color=self.graph_label_color_1)
        back_button.bind(on_press=lambda instance: self.graph_controller.back_to_menu())

        save_button = Button(text="save model", background_color=self.graph_label_color_1)
        save_button.bind(on_press=lambda instance: self.graph_controller.save_model())

        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", radius=[10])
        modelBox.add_widget(back_button)
        modelBox.add_widget(save_button)

        tool1.add_widget(modelBox)

        # display the picture of the model
        scatter = ResizableDraggablePicture(do_rotation=False, do_scale=True)

        # get the visualized graph
        if self.graph_controller.model is not None:
            self.graph_controller.image = self.graph_controller.get_visualized_graph()
        else:
            # todo placeholder picture
            self.graph_controller.image = Image(source='placeholder.png')

        scatter.add_widget(self.graph_controller.image)
        scatter.scale = 4

        layout.add_widget(scatter)

        # combine both element two one screen
        screen = Screen()
        screen.add_widget(tool1)
        screen.add_widget(layout)

        return screen

    def build_add_vertex_label_layout(self, functionName, color):
        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=color, radius=[14])
        modelBox.add_widget(MDLabel(text=functionName))
        btn2 = TextInput(text="name")
        modelBox.add_widget(btn2)

        modelBox.add_widget(MDLabel(text="source"))
        btn3 = MDCheckbox(active=False)
        modelBox.add_widget(btn3)

        modelBox.add_widget(MDLabel(text="sink"))
        btn4 = MDCheckbox(active=False)
        modelBox.add_widget(btn4)

        btn5 = Button(text='+')
        btn5.bind(on_press=lambda instance: self.graph_controller.add_vertex(btn2.text, btn3.active, btn4.active))
        modelBox.add_widget(btn5)

        return modelBox

    def build_add_edge_label_layout(self, functionName, color):
        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=color, radius=[10])
        modelBox.add_widget(MDLabel(text=functionName))
        btn2 = TextInput(text="from")
        btn3 = TextInput(text="to")
        btn4 = TextInput(text="weight")
        btn5 = Button(text='+')
        btn5.bind(on_press=lambda instance: self.graph_controller.add_edge(btn2.text, btn3.text, btn4.text))

        modelBox.add_widget(btn2)
        modelBox.add_widget(btn3)
        modelBox.add_widget(btn4)
        modelBox.add_widget(btn5)

        return modelBox

    def build_edit_vertex_label_layout(self, functionName, color):
        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=color, radius=[10])
        modelBox.add_widget(MDLabel(text=functionName))
        btn2 = TextInput(text="name")
        modelBox.add_widget(btn2)

        modelBox.add_widget(MDLabel(text="source"))
        btn3 = MDCheckbox(active=False)
        modelBox.add_widget(btn3)

        modelBox.add_widget(MDLabel(text="sink"))
        btn4 = MDCheckbox(active=False)
        modelBox.add_widget(btn4)

        modelBox.add_widget(MDLabel(text="delete"))
        btn5 = MDCheckbox(active=False)
        btn6 = Button(text='√')
        btn6.bind(on_press=lambda instance: self.graph_controller.edit_vertex(btn2.text, btn3.active, btn4.active, btn5.active))

        modelBox.add_widget(btn5)
        modelBox.add_widget(btn6)

        return modelBox

    def build_change_name_layout(self, functionName, color):
        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=color, radius=[10])
        modelBox.add_widget(MDLabel(text=functionName))
        btn2 = TextInput(text="name")
        btn3 = TextInput(text="new name")
        btn4 = Button(text='√')
        btn4.bind(on_press=lambda instance: self.graph_controller.change_name(btn2.text, btn3.text))

        modelBox.add_widget(btn2)
        modelBox.add_widget(btn3)
        modelBox.add_widget(btn4)

        return modelBox

    def build_edit_edge_label_layout(self, functionName, color):
        modelBox = MDBoxLayout(orientation='horizontal', padding='12dp', spacing="12dp", md_bg_color=color, radius=[10])
        modelBox.add_widget(MDLabel(text=functionName))
        btn2 = TextInput(text="from")
        btn3 = TextInput(text="to")
        btn4 = TextInput(text="weight")

        modelBox.add_widget(btn2)
        modelBox.add_widget(btn3)
        modelBox.add_widget(btn4)

        modelBox.add_widget(MDLabel(text="delete"))
        btn5 = MDCheckbox(active=False)
        btn6 = Button(text='√')
        btn6.bind(on_press=lambda instance: self.graph_controller.edit_edge(btn2.text, btn3.text, btn4.text, btn5.active))

        modelBox.add_widget(btn5)
        modelBox.add_widget(btn6)

        return modelBox