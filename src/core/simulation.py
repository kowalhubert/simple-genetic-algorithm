from src.config.simulation_config import SimulationConfiguration


class Simulation:
    def __init__(self, simulation_config: SimulationConfiguration) -> None:
        self.__config = simulation_config

        self._epochs_number = self.__config.general_config.epochs_no 

    def start(self):
        for epoch in range(self._epochs_number):
            print(f'Epoch {epoch + 1}')
            
        