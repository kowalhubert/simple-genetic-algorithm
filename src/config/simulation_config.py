from src.config.cost_function_config import CostFunctionConfig
from src.config.general_config import GeneralConfig
from src.config.crossing_config import CrossingConfig
from src.config.elite_strategy_config import EliteStrategyConfig
from src.config.general_config import GeneralConfig
from src.config.inversion_config import InversionConfig
from src.config.mutation_config import MutationConfig
from src.config.selection_config import SelectionConfig


class SimulationConfiguration:
    def __init__(
        self,
        cost_function_config: CostFunctionConfig, 
        crossing_config: CrossingConfig,
        elite_strategy_config: EliteStrategyConfig,
        general_config: GeneralConfig,
        inversion_config: InversionConfig,
        mutation_config: MutationConfig,
        selection_config: SelectionConfig) -> None:
        
        self.cost_function_config = cost_function_config
        self.crossing_config = crossing_config
        self.elite_strategy_config = elite_strategy_config
        self.general_config = general_config
        self.inversion_config = inversion_config
        self.mutation_config = mutation_config
        self.selection_config = selection_config

