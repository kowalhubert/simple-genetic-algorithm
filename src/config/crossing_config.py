from src.core.crossing import AbstractCrossing, CrossingMethodType, GrainCrossing, SinglePointCrossing, TwoPointCrossing, UniformCrossing


class CrossingConfig:
    def __init__(self, crossing_type: CrossingMethodType, grain: int = None):
        assert crossing_type is not None
        assert crossing_type != CrossingMethodType.GRAIN or (grain is not None and grain > 0)

        self.__grain = grain
        self.__crossing_type = crossing_type
        self.crossing_func = self._get_crossing_implementation().cross

    def _get_crossing_implementation(self) -> AbstractCrossing:
        match self.__crossing_type:
            case CrossingMethodType.SINGLE_POINT:
                return SinglePointCrossing()
            case CrossingMethodType.TWO_POINT:
                return TwoPointCrossing()
            case CrossingMethodType.UNIFORM:
                return UniformCrossing()
            case CrossingMethodType.GRAIN:
                return GrainCrossing(grain_size=self.__grain)