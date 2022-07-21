import os

from utilities.FileManager import FileManager


class SimulationManager:
    """
    An utility object to keep track of ongoing and finished simulation. Used by the SimulationController to add new
    simulations and used by the SimulationOverviewController to Query the status off a specific or all ongoing
    simulations
    """

    def __init__(self):
        self.futures = []
        self.ongoingSimulations = []
        self.mapping = {}
        self.finishedSimulations = {}
        self.fm = FileManager(os.getcwd() + "/data/")

    def view_ongoing_simulations(self):
        return self.ongoingSimulations.copy()

    def view_mappings(self):
        """
        view mappings
        """
        return self.mapping.copy()

    def view_futures(self):
        """
        view all futures
        """
        return self.futures.copy()

    def clean_up(self, simulation_name):
        """
        remove a finished simulation
        """
        simulation, future = self.mapping[simulation_name]
        self.mapping.pop(simulation_name, None)
        self.futures.remove(future)
        self.ongoingSimulations.remove(simulation)
        self.fm.removeProgress(simulation_name)

        self.finishedSimulations[simulation_name] = simulation

    def cancel_ongoing_simulation(self, simulation_name):
        """
        Is called by the SimulationController to terminate a running simulation
        """
        # get mapping pair
        simulation, future = self.mapping[simulation_name]

        # if simulation is already done clean up else cancel simulation
        if future.done():
            self.clean_up(simulation_name)
        else:
            # cancel future
            future.cancel()

            # remove from mapping, futures, tmp files and ongoing_simulations
            self.mapping.pop(simulation_name, None)
            self.futures.remove(future)
            self.ongoingSimulations.remove(simulation)
            self.fm.removeProgress(simulation_name)
