from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image

from utilities.ResizableDraggablePicture import ResizableDraggablePicture


class SimulationView:
    def __init__(self, simulation_controller):
        self.sim_controller = simulation_controller

    def build_screen(self):
        self.sim_controller.parameters = {}
        # modelbox for parameters
        layout = MDBoxLayout(orientation='vertical', radius=[10])

        parameter_form = GridLayout(cols=1,
                                    row_force_default=True,
                                    col_force_default=False,
                                    padding=[0, 0, 0, 0],
                                    row_default_height='30dp',
                                    size_hint_y=None)
        # number of traces
        number_of_traces_form = MDBoxLayout(orientation='horizontal', radius=[10])
        label = MDLabel(text="Number of traces", font_size="12dp")
        num_traces_input = TextInput(text="1000")
        self.sim_controller.parameters["Number of traces"] = num_traces_input

        number_of_traces_form.add_widget(label)
        number_of_traces_form.add_widget(num_traces_input)

        # min trace length
        min_trace_form = MDBoxLayout(orientation='horizontal', radius=[10])
        min_label = MDLabel(text="Minimal trace length")
        min_trace_input = TextInput(text="1")
        self.sim_controller.parameters["Minimal trace length"] = min_trace_input

        min_trace_form.add_widget(min_label)
        min_trace_form.add_widget(min_trace_input)

        # max trace length
        max_trace_form = MDBoxLayout(orientation='horizontal', radius=[10])
        max_label = MDLabel(text="Maximal trace length")
        max_trace_input = TextInput(text="100")
        self.sim_controller.parameters["Maximal trace length"] = max_trace_input

        max_trace_form.add_widget(max_label)
        max_trace_form.add_widget(max_trace_input)

        # noise amount
        noise_amount_form = MDBoxLayout(orientation='horizontal', radius=[10])
        noise_label = MDLabel(text="Noise in percentage")
        noise_input = TextInput(text="10")
        self.sim_controller.parameters["Noise in percentage"] = noise_input

        noise_amount_form.add_widget(noise_label)
        noise_amount_form.add_widget(noise_input)

        # noise distribution
        # insertion
        insertion_disto_form = MDBoxLayout(orientation='horizontal', radius=[10])
        insertion_disto_label = MDLabel(text="Amount of insertion")
        insertion_disto_input = TextInput(text="50.0")
        self.sim_controller.parameters["Amount of insertion"] = insertion_disto_input

        insertion_disto_form.add_widget(insertion_disto_label)
        insertion_disto_form.add_widget(insertion_disto_input)

        # deletion
        delete_disto_form = MDBoxLayout(orientation='horizontal', radius=[10])
        delete_disto_label = MDLabel(text="Amount of deletion")
        delete_disto_input = TextInput(text="25.0")
        self.sim_controller.parameters["Amount of deletion"] = delete_disto_input

        delete_disto_form.add_widget(delete_disto_label)
        delete_disto_form.add_widget(delete_disto_input)

        # modification
        modification_disto_form = MDBoxLayout(orientation='horizontal', radius=[10])
        modification_disto_label = MDLabel(text="Amount of modification")
        modification_disto_input = TextInput(text="25.0")
        self.sim_controller.parameters["Amount of modification"] = modification_disto_input

        modification_disto_form.add_widget(modification_disto_label)
        modification_disto_form.add_widget(modification_disto_input)

        parameter_form.add_widget(number_of_traces_form)
        parameter_form.add_widget(min_trace_form)
        parameter_form.add_widget(max_trace_form)
        parameter_form.add_widget(noise_amount_form)
        parameter_form.add_widget(insertion_disto_form)
        parameter_form.add_widget(delete_disto_form)
        parameter_form.add_widget(modification_disto_form)
        parameter_form.bind(minimum_height=parameter_form.setter('height'))

        start_button = Button(text="Start Simulation")
        start_button.bind(on_press=lambda x: self.sim_controller.start_simulation_button())
        parameter_form.add_widget(start_button)

        back_button = Button(text="Back to Menu")
        back_button.bind(on_press=lambda x: self.sim_controller.back_to_menu())
        parameter_form.add_widget(back_button)

        layout.add_widget(parameter_form)

        # display the picture of the model
        scatter = ResizableDraggablePicture(do_rotation=False, do_scale=True)

        if self.sim_controller.model is not None:
            # get the visualized graph
            png = self.sim_controller.model.visualise()
            image = Image(source=png)
        else:
            image = Image(source="placeholder.png")

        scatter.add_widget(image)
        scatter.scale = 4

        layout.add_widget(scatter)

        # buttons
        screen = Screen()
        screen.add_widget(layout)

        return screen
