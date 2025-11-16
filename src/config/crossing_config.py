from src.core.crossing import AbstractCrossing, CrossingMethodType, LinearCrossing, ArithmeticCrossing, AlphaBlendCrossing, AlphaBetaBlendCrossing, MeanCrossing
from src.core.unit import UnitFactory


class CrossingConfig:
    def __init__(self, crossing_type: CrossingMethodType, probability: int, unit_factory: UnitFactory, elite_count: int, grain: int = None):
        assert crossing_type is not None
        self.__crossing_type = crossing_type
        self.elite_count = elite_count
        self.probability = probability
        self.crossing_func = self._get_crossing_implementation().cross
        
        self.crossing_type = crossing_type
        self.grain = grain

    def _get_crossing_implementation(self) -> AbstractCrossing:
        match self.__crossing_type:
            case CrossingMethodType.LINEAR:
                return LinearCrossing(self.probability)
            case CrossingMethodType.ARITHMETIC:
                return ArithmeticCrossing(self.probability)
            case CrossingMethodType.ALPHA_BLEND:
                return AlphaBlendCrossing(self.probability)
            case CrossingMethodType.ALPHA_BETA_BLEND:
                return AlphaBetaBlendCrossing(self.probability)
            case CrossingMethodType.MEAN:
                return MeanCrossing(self.probability)