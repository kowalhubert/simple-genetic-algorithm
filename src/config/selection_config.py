
from src.core.selection import BestSelection, RouletteWheelSelection, TournamentSelection
from src.core.selection import SelectionMethodType

class SelectionConfig:
    def __init__(self, selection_type: SelectionMethodType, selection_percentage: int, is_maxim_case: bool = True, tournament_size: int = None):
        assert selection_type is not None
        assert selection_percentage > 0 and selection_percentage < 100
        assert selection_type != SelectionMethodType.TOURNAMENT or (tournament_size is not None and tournament_size > 1)
        
        self.is_maxim_case = is_maxim_case
        self.selection_type = selection_type
        self.selection_percentage = selection_percentage
        self.tournament_size = tournament_size

        self.selection_func = self._get_selection_implementation().select

    def _get_selection_implementation(self):
        match self.selection_type:
            case SelectionMethodType.BEST:
                return BestSelection(is_maximization=self.is_maxim_case)
            case SelectionMethodType.ROULETTE:
                return RouletteWheelSelection(is_maximization=self.is_maxim_case)
            case SelectionMethodType.TOURNAMENT:
                return TournamentSelection(is_maximization=self.is_maxim_case, tournament_size=self.tournament_size)