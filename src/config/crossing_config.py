from src.core.crossing import AbstractCrossing, CrossingMethodType, GrainCrossing, SinglePointCrossing, TwoPointCrossing, UniformCrossing
from src.core.unit import UnitFactory


class CrossingConfig:
    def __init__(self, crossing_type: CrossingMethodType, probability: int, unit_factory: UnitFactory, elite_count: int, grain: int = None):
        assert crossing_type is not None
        assert crossing_type != CrossingMethodType.GRAIN or (grain is not None and grain > 0)

        self.__grain = grain
        self.__crossing_type = crossing_type
        self.__unit_factory = unit_factory
        self.elite_count = elite_count
        self.probability = probability
        self.crossing_func = self._get_crossing_implementation().cross
        
        # Public properties for serialization
        self.crossing_type = crossing_type
        self.grain = grain

    def _get_crossing_implementation(self) -> AbstractCrossing:
        match self.__crossing_type:
            case CrossingMethodType.SINGLE_POINT:
                return SinglePointCrossing(self.probability, self.__unit_factory)
            case CrossingMethodType.TWO_POINT:
                return TwoPointCrossing(self.probability, self.__unit_factory)
            case CrossingMethodType.UNIFORM:
                return UniformCrossing(self.probability, self.__unit_factory)
            case CrossingMethodType.GRAIN:
                return GrainCrossing(self.probability, self.__unit_factory, self.__grain)