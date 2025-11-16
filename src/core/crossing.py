from src.core.unit import Unit
from abc import ABC, abstractmethod
from enum import Enum
import random

class CrossingMethodType(Enum):
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
    
class ArithmeticCrossing(AbstractCrossing):
    def __init__(self, probability: int, alpha: float = 0.5):
        super().__init__(probability) 
        self.alpha = alpha

    def _perform_cross(self, parent1: Unit, parent2: Unit):
        a = self.alpha

        child1 = [
            a * x + (1 - a) * y
            for x, y in zip(parent1.real_values, parent2.real_values)
        ]

        child2 = [
            a * y + (1 - a) * x
            for x, y in zip(parent1.real_values, parent2.real_values)
        ]

        return Unit(real_values=child1), Unit(real_values=child2)

class LinearCrossing(AbstractCrossing):
    def __init__(self, probability: int):
        super().__init__(probability)

    def _perform_cross(self, parent1: Unit, parent2: Unit):
        x = parent1.real_values
        y = parent2.real_values

        Z = [(0.5 * xi + 0.5 * yi) for xi, yi in zip(x, y)]
        V = [(1.5 * xi - 0.5 * yi) for xi, yi in zip(x, y)]
        W = [(-0.5 * xi + 1.5 * yi) for xi, yi in zip(x, y)]

        return [Unit(real_values=Z), Unit(real_values=V), Unit(real_values=W)]

class AlphaBlendCrossing(AbstractCrossing):
    def __init__(self, probability: int, alpha: float = 0.5):
        super().__init__(probability)
        self.alpha = alpha

    def _perform_cross(self, parent1: Unit, parent2: Unit):
        child1 = []
        child2 = []

        for x, y in zip(parent1.real_values, parent2.real_values):
            d = abs(x - y)

            low = min(x, y) - self.alpha * d
            high = max(x, y) + self.alpha * d

            c1 = random.uniform(low, high)
            c2 = random.uniform(low, high)

            child1.append(c1)
            child2.append(c2)

        return Unit(real_values=child1), Unit(real_values=child2)

class AlphaBetaBlendCrossing(AbstractCrossing):
    def __init__(self, probability: int, alpha: float = 0.3, beta: float = 0.7):
        super().__init__(probability)
        self.alpha = alpha
        self.beta = beta

    def _perform_cross(self, parent1: Unit, parent2: Unit):
        child1 = []
        child2 = []

        for x, y in zip(parent1.real_values, parent2.real_values):
            d = abs(x - y)

            low = min(x, y) - self.alpha * d
            high = max(x, y) + self.beta * d

            c1 = random.uniform(low, high)
            c2 = random.uniform(low, high)

            child1.append(c1)
            child2.append(c2)

        return Unit(real_values=child1), Unit(real_values=child2)

class MeanCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        mean_values = [(x + y) / 2 for x, y in zip(parent1.real_values, parent2.real_values)]
        return Unit(real_values=mean_values), Unit(real_values=mean_values)