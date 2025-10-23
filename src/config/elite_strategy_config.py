from src.core.elite_strategy import EliteStrategy


class EliteStrategyConfig:
    def __init__(self, elite_count: int):
        assert elite_count is not None and elite_count >= 0, "elite_count must be non-negative integer"

        self.__elite_count = elite_count
        self.elite_selection_func = EliteStrategy(elite_count).select_elite
        
