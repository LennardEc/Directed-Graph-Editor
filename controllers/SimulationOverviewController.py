from kivy.uix.screenmanager import Screen

from views.simulation.SimulationOverviewScreen import SimulationOverviewScreen

tool_bar_skeleton = """
MDToolbar:
    title: "Simulation Overview"
"""

class SimulationOverviewController(Screen):

    def set_parameters(self, screen_manager, screens, simulation_manager):
        self.screen_manager = screen_manager
        self.screens = screens
        self.simulation_manager = simulation_manager

    def __init__(self, **kw):
        super().__init__(**kw)

        self.screen_manager = None
        self.screens = None
        self.simulation_manager = None
        self.screen_builder = SimulationOverviewScreen(self)

        self.graph_box_color = [41 / 255, 162 / 255, 162 / 255, 1]
        self.log_box_color = [41 / 255, 162 / 255, 162 / 255, 1]

        self.graph_box_color_1 = [153 / 255, 157 / 255, 157 / 255, 1]
        self.log_box_color_1 = [153 / 255, 157 / 255, 157 / 255, 1]

        self.current_screen = self.screen_builder.build_empty_screen()
        self.add_widget(self.current_screen)

    def on_pre_enter(self, *args):
        self.remove_widget(self.current_screen)
        self.current_screen = self.screen_builder.build_screen()
        self.add_widget(self.current_screen)

    def back_to_menu(self):
        self.screen_manager.switch_to(self.screens[0])
