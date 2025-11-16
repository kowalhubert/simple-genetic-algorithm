from src.core.unit import Unit, UnitFactory
from abc import ABC, abstractmethod
from enum import Enum
import random

class MutationMethodType(Enum):
    UNIFORM = "Uniform"
    GAUSSIAN = "Gaussian"

class AbstractMutation(ABC):
    def __init__(self, probability: float, unit_factory: UnitFactory):
        self.probability = probability
        self.unit_factory = unit_factory

    @abstractmethod
    def mutate(self, unit: Unit) -> Unit:
        pass
    
class UniformMutation(AbstractMutation):
    def mutate(self, unit: Unit) -> Unit:
        new_values = unit.real_values.copy()
        for i in range(len(new_values)):
            if random.random() < self.probability / 100:
                new_values[i] = random.uniform(self.unit_factory._lower_bound,
                                               self.unit_factory._upper_bound)
        return Unit(real_values=new_values, cost=unit.cost)

class GaussianMutation(AbstractMutation):
    def __init__(self, probability: float, unit_factory: UnitFactory, sigma: float):
        super().__init__(probability, unit_factory)
        self.sigma = sigma 

    def mutate(self, unit: Unit) -> Unit:
        new_values = unit.real_values.copy()
        for i in range(len(new_values)):
            if random.random() < self.probability / 100:
                new_values[i] += random.gauss(0, self.sigma)
                new_values[i] = max(self.unit_factory._lower_bound,
                                    min(self.unit_factory._upper_bound, new_values[i]))
        return Unit(real_values=new_values, cost=unit.cost)