from src.core.mutation import AbstractMutation, MutationMethodType, BoundaryMutation, TwoPointMutation, SinglePointMutation
from src.core.unit import UnitFactory


class MutationConfig:
    def __init__(self, unit_factory: UnitFactory, mutation_type: MutationMethodType, probability: int):
        assert mutation_type is not None
        assert probability > 0 and probability < 100

        self.__unit_factory = unit_factory
        self.__mutation_type = mutation_type
        self.__probability = probability

        self.mutation_func = self._get_mutation_implementation().mutate
        
        # Public properties for serialization
        self.mutation_type = mutation_type
        self.probability = probability
        
    def _get_mutation_implementation(self) -> AbstractMutation:
        match self.__mutation_type:
            case MutationMethodType.SINGLE_POINT:
                return SinglePointMutation(self.__probability, self.__unit_factory)
            case MutationMethodType.TWO_POINT:
                return TwoPointMutation(self.__probability, self.__unit_factory)
            case MutationMethodType.BOUNDARY:
                return BoundaryMutation(self.__probability, self.__unit_factory)