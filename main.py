

if __name__ == '__main__':
    import os

    from controllers.ViewLogController import ViewLogController
    from controllers.GraphController import GraphController
    from controllers.ViewGraphController import ViewGraphController
    from controllers.SimulationOverviewController import SimulationOverviewController
    from controllers.DefaultController import DefaultController
    from controllers.SimulationController import SimulationController

    from utilities.SimulationManager import SimulationManager
    from utilities.FileManager import FileManager

    from kivy.uix.popup import Popup
    from kivy.uix.textinput import TextInput
    from kivymd.app import MDApp
    from kivy.uix.button import Button
    from kivy.core.window import Window
    from kivy.uix.screenmanager import Screen, ScreenManager
    from kivy.uix.screenmanager import NoTransition
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivy.lang import Builder

    Builder.load_string(
    """
<DefaultController>:

<NameModelPopUp>:

<SettingsScreen>:

<GraphController>:

<LogController>:

<SimulationController>:

<SimulationOverviewController>:
    """)

    class NameModelPopUp(Screen):
        def __init__(self, **kw):
            super().__init__(**kw)

            self.screen_manager = None
            self.screens = None

            self.fm = FileManager(self.get_data_dir())

            # txt field
            self.txt_input = TextInput(multiline=False)
            self.txt_input.bind(text=self.on_text)

            # continue button
            self.continue_btn = Button(text="continue", disabled=True)

            # back button
            back_btn = Button(text="back")
            back_btn.bind(on_press=lambda x: self.back_to_home())

            bl = MDBoxLayout(orientation='vertical')
            bl.add_widget(self.txt_input)
            bl.add_widget(self.continue_btn)
            bl.add_widget(back_btn)

            popup = Popup(title='Enter a model name: ',
                          content=bl,
                          size_hint=(0.5, 0.5),
                          pos_hint={'right': .75, 'top': .75},
                          size=(400, 400))

            self.add_widget(popup)

        def on_text(self, instance, value):
            if not (value in self.fm.graphFolders) and value != "":
                self.continue_btn.disabled = False
                self.continue_btn.bind(on_press=lambda x: self.enter_editor(self.txt_input.text))
            else:
                self.continue_btn.disabled = True

        # todo editor screen position
        def enter_editor(self, value):
            editor = self.screens[4]
            editor.initialize_model(value)
            self.screen_manager.switch_to(self.screens[4])

        def back_to_home(self):
            self.screen_manager.switch_to(self.screens[0])

        def set_parameters(self, screen_manager, screens):
            self.screen_manager = screen_manager
            self.screens = screens

        def get_data_dir(self):
            path = os.getcwd() + "\data\\"
            if os.path.isdir(path):
                return path
            else:
                return os.getcwd() + "/data/"


    class DirectedGraph(MDApp):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.sm = None
            self.screen = None
            Window.size = (1000, 700)

        def on_stop(self):
            # on stop clean tmp folder
            FileManager(os.getcwd() + "/data/").cleanProgress()

        def build(self):
            # list of all screen objects
            screens = []

            # screen manager
            sm = ScreenManager()
            sm.transition = NoTransition()

            # screen 1
            dft = DefaultController(name='defaultController')
            screens.append(dft)
            sm.add_widget(dft)

            # screen 2
            nmpu = NameModelPopUp(name="popup")
            screens.append(nmpu)
            sm.add_widget(nmpu)

            # screens 3
            sets = SimulationController(name='simulations')
            screens.append(sets)
            sm.add_widget(sets)

            # screens 4
            sim_over = SimulationOverviewController(name="simulation")
            screens.append(sim_over)
            sm.add_widget(sim_over)

            # screens 5
            editor = GraphController(name="editor")
            screens.append(editor)
            sm.add_widget(editor)

            # screen 6
            view_graph = ViewGraphController(name="view model")
            screens.append(view_graph)
            sm.add_widget(view_graph)

            # screen 7
            view_log = ViewLogController(name="view log")
            screens.append(view_log)
            sm.add_widget(view_log)

            simulation_manager = SimulationManager()
            # pass parameters
            dft.set_parameters(sm, screens)
            sets.set_parameters(sm, screens, simulation_manager)
            nmpu.set_parameters(sm, screens)
            sim_over.set_parameters(sm, screens, simulation_manager)
            editor.set_parameters(sm, screens)
            view_graph.set_parameters(sm, screens)
            view_log.set_parameters(sm, screens)

            self.sm = sm
            self.screen = screens

            return sm


    DirectedGraph().run()
