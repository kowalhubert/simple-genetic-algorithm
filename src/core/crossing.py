from abc import ABC, abstractmethod
from enum import Enum
import random

class CrossingMethodType(Enum):
    SINGLE_POINT = "Single-point"
    TWO_POINT = "Two-point"
    UNIFORM = "Uniform"
    GRAIN = "Grain"

class AbstractCrossing(ABC):
    @abstractmethod
    def cross(self, parent1, parent2, **kwargs):
        pass

class SinglePointCrossing(AbstractCrossing):
    def cross(self, parent1, parent2, **kwargs):
        # Assume parent1 and parent2 are list-like (e.g., lists of genes)
        length = len(parent1)
        if length < 2:
            return parent1[:], parent2[:]
        point = random.randint(1, length - 1)
        offspring1 = parent1[:point] + parent2[point:]
        offspring2 = parent2[:point] + parent1[point:]
        return offspring1, offspring2

class TwoPointCrossing(AbstractCrossing):
    def cross(self, parent1, parent2, **kwargs):
        length = len(parent1)
        if length < 3:
            return parent1[:], parent2[:]
        point1 = random.randint(1, length - 2)
        point2 = random.randint(point1 + 1, length - 1)
        offspring1 = (
            parent1[:point1]
            + parent2[point1:point2]
            + parent1[point2:]
        )
        offspring2 = (
            parent2[:point1]
            + parent1[point1:point2]
            + parent2[point2:]
        )
        return offspring1, offspring2

class UniformCrossing(AbstractCrossing):
    # todos
    def cross(self, parent1, parent2, **kwargs):
        length = len(parent1)
        mask = [random.randint(0, 1) for _ in range(length)]
        offspring1 = [parent1[i] if mask[i] else parent2[i] for i in range(length)]
        offspring2 = [parent2[i] if mask[i] else parent1[i] for i in range(length)]
        return offspring1, offspring2

class GrainCrossing(AbstractCrossing):
    def __init__(self, grain_size=2):
        self.grain_size = grain_size

    def cross(self, parent1, parent2, **kwargs):
        # "Grain" means crossover in fixed-size segments.
        length = len(parent1)
        offspring1 = []
        offspring2 = []
        toggle = True
        for i in range(0, length, self.grain_size):
            if toggle:
                offspring1.extend(parent1[i:i+self.grain_size])
                offspring2.extend(parent2[i:i+self.grain_size])
            else:
                offspring1.extend(parent2[i:i+self.grain_size])
                offspring2.extend(parent1[i:i+self.grain_size])
            toggle = not toggle
        return offspring1, offspring2
