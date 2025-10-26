from ast import List
from math import floor
import random
from src.config.simulation_config import SimulationConfiguration
from src.core.selection import SelectionMethodType
from src.core.unit import Unit


class Simulation:
    def __init__(self, simulation_config: SimulationConfiguration) -> None:
        self._config = simulation_config

        self._population = []

        self._cost_function = self._config.cost_function_config.cost_func
        self._population_size = self._config.general_config.population_size
        self._dimesions = self._config.cost_function_config.dimensions
        self._bounds = self._config.cost_function_config.cost_func.suggested_bounds()
        self._epochs_number = self._config.general_config.epochs_no 

        self._unit_factory = simulation_config.unit_factory

        self._selection_num = self._calculate_selection_size()
        self._selection_func = self._config.selection_config.selection_func

        self._is_maximim_case = self._config.selection_config.is_maxim_case

        self._elite_units_count = self._config.crossing_config.elite_count
        self._crossing_func = self._config.crossing_config.crossing_func

        self._mutation_func = self._config.mutation_config.mutation_func

        self._inversion_func = self._config.inversion_config.inversion_func

    def start(self):
        # generate init values
        self._generate_init_population()

        for epoch in range(self._epochs_number):
            print(f'Epoch {epoch + 1}')
            
            # calculate cost function for each from the population
            self._calculate_costs()

            # select elite units

            # select units from population to cross
            selected_units = self._selection_func(self._population, self._selection_num)

            # INSERT_YOUR_CODE
            # Extract the best elite units from selected_units
            print(len(selected_units))
            selected_units_sorted = sorted(selected_units, key=lambda ind: ind.cost, reverse=self._is_maximim_case) 

            elites = selected_units_sorted[:self._elite_units_count]
            rest_selected = selected_units_sorted[self._elite_units_count:]

            # cross selected units
            crossed_units = self._cross_selected_units(rest_selected)
            
            # mutate crossed units
            mutated_units = self._mutate_units(crossed_units)
            mutated_units.extend(elites)

            # inverse
            self._population = self._inverse_units(mutated_units)
        
        self._calculate_costs()
    
    def _calculate_selection_size(self) -> int:
        if SelectionMethodType.TOURNAMENT == self._config.selection_config.selection_type:
            return self._config.selection_config.tournament_size

        selection_percentage = float(self._config.selection_config.selection_percentage) / 100
        return int(floor(self._population_size * selection_percentage))

    def _generate_init_population(self):
        self._population = []
        
        lower_bounds = [self._bounds[0][i] for i in range(self._dimesions)]
        upper_bounds = [self._bounds[1][i] for i in range(self._dimesions)]

        for _ in range(self._population_size):
            individual = []
            for dim in range(self._dimesions):
                val = random.uniform(lower_bounds[dim], upper_bounds[dim])
                individual.append(val)
            self._population.append(self._unit_factory.create_unit_with_real_values(individual))
            
    def _calculate_costs(self):
        for unit in self._population:
            unit.cost = self._cost_function(unit.real_values)

    def _cross_selected_units(self, selected_units: int):
        new_population = []
        num_offspring = self._population_size - self._elite_units_count

        while len(new_population) < num_offspring:
            # Randomly pick two parents
            parent1, parent2 = random.sample(selected_units, 2)
            # crossing_func is expected to return a tuple: (new1, new2)
            new1, new2 = self._crossing_func(parent1, parent2)
            for child in (new1, new2):
                if len(new_population) < num_offspring:
                    new_population.append(child)
                else:
                    break
        return new_population

    def _mutate_units(self, crossed_units: list[Unit]) -> list[Unit]:
        return [self._mutation_func(unit) for unit in crossed_units]

    def _inverse_units(self, mutated_units: list[Unit]) -> list[Unit]:
        return [self._inversion_func(unit) for unit in mutated_units]