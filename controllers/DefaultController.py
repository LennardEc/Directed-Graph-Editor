import os

from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from utilities.FileManager import FileManager
from views.default.DefaultScreen import DefaultScreen


class DefaultController(Screen):
    @property
    def build_screen(self):
        dfs = DefaultScreen(self)
        return dfs.build_screen()

    def __init__(self, **kw):
        super().__init__(**kw)

        self.screen_manager = None
        self.screens = None

        # create filemanager to load existing models and logs
        self.fm = FileManager(os.getcwd() + "/data/")

        # remove all tmp files from previous sessions
        self.fm.cleanProgress()

        # current version of the displayed screen
        self.current_screen_build = self.build_screen
        self.add_widget(self.current_screen_build)

    # rebuild the screen to show new logs and graphs
    def on_pre_enter(self, *args):
        self.remove_widget(self.current_screen_build)
        self.fm.refresh()
        self.current_screen_build = self.build_screen
        self.add_widget(self.current_screen_build)

    # redirect to the simulation overview
    def simulation_overview(self):
        """
        outside of the scope for the project
        """
        sim = self.screens[3]
        self.screen_manager.switch_to(sim)

    # model callback functions
    def edit_model(self, modelName):
        editor = self.screens[4]
        editor.initialize_model(modelName)
        self.screen_manager.switch_to(editor)

    def view_model(self, modlName):
        view = self.screens[5]
        view.initialize_model(modlName)
        self.screen_manager.switch_to(view)

    def simulate_model(self, modelName):
        sim = self.screens[2]
        sim.initialize_model(modelName)
        self.screen_manager.switch_to(sim)

    def collaborate_model(self, modelName):
        """
        outside the scope of the project
        """
        print("collaborate: " + modelName)

    # log call back functions
    def view_log(self, logName):
        log = self.screens[6]
        log.initialize_model(logName)
        self.screen_manager.switch_to(log)

    def model_log(self, logName):
        _, meta_dict = self.fm.loadLog(logName)
        name = meta_dict['name of the model']
        if name in self.fm.graphFolders:
            view = self.screens[5]
            view.initialize_model(name)
            self.screen_manager.switch_to(view)
        else:
            dia = MDDialog(title="Model doesn't exists anymore!")
            dia.open()


    def share_log(self, logName):
        """
        outside the scope of the project
        """
        print("collaborate: " + logName)

    def set_parameters(self, screen_manager, screens):
        self.screen_manager = screen_manager
        self.screens = screens

    # callback for toolbar TODO dont hardcode transitions
    def create_model(self):
        self.screen_manager.switch_to(self.screens[1])
