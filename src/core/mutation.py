from src.core.unit import Unit, UnitFactory
from abc import ABC, abstractmethod
from enum import Enum
import random

class MutationMethodType(Enum):
    BOUNDARY = "Boundary"
    SINGLE_POINT = "Single-point"
    TWO_POINT = "Two-point"
    UNIFORM = "Uniform"
    GAUSSIAN = "Gaussian"

class AbstractMutation(ABC):
    def __init__(self, probability: float, unit_factory: UnitFactory):
        self.probability = probability
        self.unit_factory = unit_factory

    @abstractmethod
    def mutate(self, unit: Unit) -> Unit:
        pass

class BoundaryMutation(AbstractMutation):
    def mutate(self, unit: Unit) -> Unit:
        new_values = unit.real_values.copy()
        for i in range(len(new_values)):
            if random.random() < self.probability / 100:
                new_values[i] = random.choice([self.unit_factory._lower_bound,
                                               self.unit_factory._upper_bound])
        return Unit(real_values=new_values, cost=unit.cost)

class SinglePointMutation(AbstractMutation):
    def mutate(self, unit: Unit) -> Unit:
        new_values = unit.real_values.copy()
        if random.random() < self.probability / 100:
            idx = random.randint(0, len(new_values) - 1)
            new_values[idx] = random.uniform(self.unit_factory._lower_bound, self.unit_factory._upper_bound)
        return Unit(real_values=new_values, cost=unit.cost)

class TwoPointMutation(AbstractMutation):
    def mutate(self, unit: Unit) -> Unit:
        new_values = unit.real_values.copy()
        if random.random() < self.probability / 100:
            if len(new_values) < 2:
                idx1 = idx2 = 0
            else:
                idx1, idx2 = sorted(random.sample(range(len(new_values)), 2))
            for i in range(idx1, idx2 + 1):
                new_values[i] = random.uniform(self.unit_factory._lower_bound, self.unit_factory._upper_bound)
        return Unit(real_values=new_values, cost=unit.cost)
    
class UniformMutation(AbstractMutation):
    def mutate(self, unit: Unit) -> Unit:
        new_values = unit.real_values.copy()
        for i in range(len(new_values)):
            if random.random() < self.probability / 100:
                # losowa wartość w całym zakresie
                new_values[i] = random.uniform(self.unit_factory._lower_bound,
                                               self.unit_factory._upper_bound)
        return Unit(real_values=new_values, cost=unit.cost)

class GaussianMutation(AbstractMutation):
    def __init__(self, probability: float, unit_factory: UnitFactory, sigma: float):
        super().__init__(probability, unit_factory)
        self.sigma = sigma  # odchylenie standardowe Gaussa

    def mutate(self, unit: Unit) -> Unit:
        new_values = unit.real_values.copy()
        for i in range(len(new_values)):
            if random.random() < self.probability / 100:
                # dodaj losowy szum Gaussa
                new_values[i] += random.gauss(0, self.sigma)
                # ograniczenie wartości do granic
                new_values[i] = max(self.unit_factory._lower_bound,
                                    min(self.unit_factory._upper_bound, new_values[i]))
        return Unit(real_values=new_values, cost=unit.cost)