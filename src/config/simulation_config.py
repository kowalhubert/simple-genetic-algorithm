from src.core.cost_function import CostFunctionConfig
from typing import Optional

class SimulationConfiguration:
    def __init__(self, population_size: int, epochs_no: int, cost_function_config: CostFunctionConfig) -> None:
        self.population_size = population_size
        self.epochs_no = epochs_no
        self.cost_function_config = cost_function_config
        
    def validate(self) -> bool:
        """Validate the simulation configuration"""
        if self.population_size <= 0:
            return False
        if self.epochs_no <= 0:
            return False
        return True

class SelectionConfig:
    def __init__(self, selection_type: str, tournament_size: Optional[int] = None):
        assert selection_type is not None

        self.selection_type = selection_type
        self.tournament_size = tournament_size

class CrossingConfig:
    def __init__(self, crossing_type: str, probability: float):
        self.crossing_type = crossing_type
        self.probability = probability

class MutationConfig:
    def __init__(self, mutation_type: str, probability: float):
        self.mutation_type = mutation_type
        self.probability = probability

class InversionConfig:
    def __init__(self, probability: float):
        self.probability = probability

class ElitaryStrategyConfig:
    def __init__(self, percentage: float):
        self.percentage = percentage
