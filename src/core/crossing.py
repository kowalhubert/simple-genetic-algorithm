from src.core.unit import Unit
from abc import ABC, abstractmethod
from enum import Enum
import random

class CrossingMethodType(Enum):
    SINGLE_POINT = "Single-point"
    TWO_POINT = "Two-point"
    UNIFORM = "Uniform"
    GRAIN = "Grain"
    LINEAR = "Linear"
    ARITHMETIC = "Arithmetic"
    ALPHA_BLEND = "Alpha Blend"
    ALPHA_BETA_BLEND = "Alpha-Beta Blend"
    MEAN = "Mean"

class AbstractCrossing(ABC):
    def __init__(self, probability: int):
        self.probability = probability

    def cross(self, parent1: Unit, parent2: Unit) -> tuple[Unit, Unit]:
        if random.randint(1, 100) <= self.probability:
            return self._perform_cross(parent1, parent2)
        else:
            return parent1, parent2

    @abstractmethod
    def _perform_cross(self, parent1: Unit, parent2: Unit) -> tuple[Unit, Unit]:
        pass

class SinglePointCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        dim = len(parent1.real_values)
        if dim < 2:
            return parent1, parent2
        point = random.randint(1, dim - 1)
        child1 = parent1.real_values[:point] + parent2.real_values[point:]
        child2 = parent2.real_values[:point] + parent1.real_values[point:]
        return Unit(real_values=child1), Unit(real_values=child2)

class TwoPointCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        dim = len(parent1.real_values)
        if dim < 3:
            return SinglePointCrossing(self.probability)._perform_cross(parent1, parent2)
        p1, p2 = sorted(random.sample(range(1, dim), 2))
        child1 = parent1.real_values[:p1] + parent2.real_values[p1:p2] + parent1.real_values[p2:]
        child2 = parent2.real_values[:p1] + parent1.real_values[p1:p2] + parent2.real_values[p2:]
        return Unit(real_values=child1), Unit(real_values=child2)

class UniformCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        dim = len(parent1.real_values)
        child1 = []
        child2 = []
        for i in range(dim):
            if random.random() < 0.5:
                child1.append(parent1.real_values[i])
                child2.append(parent2.real_values[i])
            else:
                child1.append(parent2.real_values[i])
                child2.append(parent1.real_values[i])
        return Unit(real_values=child1), Unit(real_values=child2)

class GrainCrossing(AbstractCrossing):
    def __init__(self, probability: int, grain_size: int = 2):
        super().__init__(probability)
        self.grain_size = grain_size

    def _perform_cross(self, parent1: Unit, parent2: Unit):
        dim = len(parent1.real_values)
        g = self.grain_size
        child1 = []
        child2 = []
        toggle = False
        for i in range(0, dim, g):
            src1 = parent1.real_values if not toggle else parent2.real_values
            src2 = parent2.real_values if not toggle else parent1.real_values
            child1.extend(src1[i:i+g])
            child2.extend(src2[i:i+g])
            toggle = not toggle
        return Unit(real_values=child1), Unit(real_values=child2)
    
class ArithmeticCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        child1 = [(x + y) / 2 for x, y in zip(parent1.real_values, parent2.real_values)]
        child2 = [(x + y) / 2 for x, y in zip(parent1.real_values, parent2.real_values)]
        return Unit(real_values=child1), Unit(real_values=child2)

class LinearCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        child1 = [0.75*x + 0.25*y for x, y in zip(parent1.real_values, parent2.real_values)]
        child2 = [0.25*x + 0.75*y for x, y in zip(parent1.real_values, parent2.real_values)]
        return Unit(real_values=child1), Unit(real_values=child2)

class AlphaBlendCrossing(AbstractCrossing):
    def __init__(self, probability: int, alpha: float = 0.5):
        super().__init__(probability)
        self.alpha = alpha

    def _perform_cross(self, parent1: Unit, parent2: Unit):
        child1 = [self.alpha*x + (1 - self.alpha)*y for x, y in zip(parent1.real_values, parent2.real_values)]
        child2 = [self.alpha*y + (1 - self.alpha)*x for x, y in zip(parent1.real_values, parent2.real_values)]
        return Unit(real_values=child1), Unit(real_values=child2)

class AlphaBetaBlendCrossing(AbstractCrossing):
    def __init__(self, probability: int, alpha: float = 0.3, beta: float = 0.7):
        super().__init__(probability)
        self.alpha = alpha
        self.beta = beta

    def _perform_cross(self, parent1: Unit, parent2: Unit):
        child1 = [self.alpha*x + (1 - self.alpha)*y for x, y in zip(parent1.real_values, parent2.real_values)]
        child2 = [self.beta*x + (1 - self.beta)*y for x, y in zip(parent1.real_values, parent2.real_values)]
        return Unit(real_values=child1), Unit(real_values=child2)

class MeanCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        mean_values = [(x + y) / 2 for x, y in zip(parent1.real_values, parent2.real_values)]
        return Unit(real_values=mean_values), Unit(real_values=mean_values)