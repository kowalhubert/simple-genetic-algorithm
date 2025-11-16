from src.core.mutation import AbstractMutation, MutationMethodType, UniformMutation, GaussianMutation
from src.core.unit import UnitFactory


class MutationConfig:
    def __init__(self, unit_factory: UnitFactory, mutation_type: MutationMethodType,
                 probability: int, sigma: float = 0.1): 
        assert mutation_type is not None
        assert 0 < probability < 100

        self.__unit_factory = unit_factory
        self.__mutation_type = mutation_type
        self.__probability = probability
        self.__sigma = sigma

        self.mutation_func = self._get_mutation_implementation().mutate
        
        self.mutation_type = mutation_type
        self.probability = probability
        
    def _get_mutation_implementation(self) -> AbstractMutation:
        match self.__mutation_type:
            case MutationMethodType.UNIFORM:
                return UniformMutation(self.__probability, self.__unit_factory)
            case MutationMethodType.GAUSSIAN:
                return GaussianMutation(self.__probability, self.__unit_factory, sigma=self.__sigma)