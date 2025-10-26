from src.config.cost_function_config import CostFunctionConfig
from src.config.general_config import GeneralConfig
from src.config.crossing_config import CrossingConfig
from src.config.general_config import GeneralConfig
from src.config.inversion_config import InversionConfig
from src.config.mutation_config import MutationConfig
from src.config.selection_config import SelectionConfig
from src.core.unit import UnitFactory


class SimulationConfiguration:
    def __init__(
        self,
        unit_factory: UnitFactory,
        cost_function_config: CostFunctionConfig, 
        crossing_config: CrossingConfig,
        general_config: GeneralConfig,
        inversion_config: InversionConfig,
        mutation_config: MutationConfig,
        selection_config: SelectionConfig) -> None:

        self.unit_factory = unit_factory
        self.cost_function_config = cost_function_config
        self.crossing_config = crossing_config
        self.general_config = general_config
        self.inversion_config = inversion_config
        self.mutation_config = mutation_config
        self.selection_config = selection_config
