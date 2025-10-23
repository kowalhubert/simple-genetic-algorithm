
from src.core.selection import BestSelection, RouletteWheelSelection, TournamentSelection
from src.core.selection import SelectionMethodType

class SelectionConfig:
    def __init__(self, selection_type: SelectionMethodType, selection_percentage: int, tournament_size: int = None):
        assert selection_type is not None
        assert selection_percentage > 0 and selection_percentage < 100
        assert tournament_size > 1
        assert selection_type != SelectionMethodType.TOURNAMENT or tournament_size is not None
        
        self.selection_type = selection_type
        self.selection_percentage = selection_percentage
        self.tournament_size = tournament_size

        self.selection_func = self._get_selection_func()

    def _get_selection_func(self):
        match self.selection_type:
            case SelectionMethodType.BEST:
                return BestSelection()
            case SelectionMethodType.ROULETTE:
                return RouletteWheelSelection()
            case SelectionMethodType.TOURNAMENT:
                return TournamentSelection(self.tournament_size)