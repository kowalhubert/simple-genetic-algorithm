from src.core.unit import UnitFactory
from abc import ABC, abstractmethod
from enum import Enum
import random
import math

from src.core.unit import Unit

class CrossingMethodType(Enum):
    SINGLE_POINT = "Single-point"
    TWO_POINT = "Two-point"
    UNIFORM = "Uniform"
    GRAIN = "Grain"

class AbstractCrossing(ABC):
    def __init__(self, probability: int, unit_factory: 'UnitFactory'):
        self.probability = probability
        self.unit_factory = unit_factory

    def cross(self, parent1: Unit, parent2: Unit,) -> tuple[Unit, Unit]:
        if random.randint(1, 100) <= self.probability:
            return self._perform_cross(parent1, parent2)
        else:
            return parent1, parent2
        pass

    @abstractmethod
    def _perform_cross(self, parent1: Unit, parent2: Unit,) -> tuple[Unit, Unit]:
        pass

class SinglePointCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        dim = len(parent1.real_values)
        if dim < 2:
            return parent1, parent2
        point = random.randint(1, dim - 1)

        child1_binaries = []
        child2_binaries = []

        for d in range(dim):
            ch1_bin_chain = parent1.binary_values[d][:point] + parent2.binary_values[d][point:] 
            ch2_bin_chain = parent2.binary_values[d][:point] + parent1.binary_values[d][point:]
        
            child1_binaries.append(ch1_bin_chain)
            child2_binaries.append(ch2_bin_chain)

        return (self.unit_factory.create_unit_with_binary_values(child1_binaries),
                self.unit_factory.create_unit_with_binary_values(child2_binaries))

class TwoPointCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        dim = len(parent1.real_values)
        if dim < 3:
            return SinglePointCrossing(self.probability, self.unit_factory).cross(parent1, parent2)
        # choose two points not at ends, so 1 .. dim-1
        p1, p2 = sorted(random.sample(range(1, dim), 2))
        child1_binaries = []
        child2_binaries = []
        for d in range(dim):
            if d < p1:
                child1_binaries.append(parent1.binary_values[d])
                child2_binaries.append(parent2.binary_values[d])
            elif d < p2:
                child1_binaries.append(parent2.binary_values[d])
                child2_binaries.append(parent1.binary_values[d])
            else:
                child1_binaries.append(parent1.binary_values[d])
                child2_binaries.append(parent2.binary_values[d])
        return (self.unit_factory.create_unit_with_binary_values(child1_binaries),
                self.unit_factory.create_unit_with_binary_values(child2_binaries))

class UniformCrossing(AbstractCrossing):
    def _perform_cross(self, parent1: Unit, parent2: Unit):
        dim = len(parent1.real_values)
        child1_binaries = []
        child2_binaries = []
        for d in range(dim):
            if random.random() < 0.5:
                child1_binaries.append(parent1.binary_values[d])
                child2_binaries.append(parent2.binary_values[d])
            else:
                child1_binaries.append(parent2.binary_values[d])
                child2_binaries.append(parent1.binary_values[d])
        return (self.unit_factory.create_unit_with_binary_values(child1_binaries),
                self.unit_factory.create_unit_with_binary_values(child2_binaries))

class GrainCrossing(AbstractCrossing):
    def __init__(self, probablity: int, unit_factory: 'UnitFactory', grain_size: int = 2):
        super().__init__(probablity, unit_factory)
        self.grain_size = grain_size

    def _perform_cross(self, parent1: Unit, parent2: Unit):
        dim = len(parent1.real_values)
        child1_binaries = []
        child2_binaries = []
        g = self.grain_size
        for d in range(dim):
            bin_len = len(parent1.binary_values[d])
            child1_bin = []
            child2_bin = []
            toggle = False
            for i in range(0, bin_len, g):
                src1 = parent1.binary_values[d] if not toggle else parent2.binary_values[d]
                src2 = parent2.binary_values[d] if not toggle else parent1.binary_values[d]
                child1_bin.extend(list(src1[i:i+g]))
                child2_bin.extend(list(src2[i:i+g]))
                toggle = not toggle
            child1_binaries.append(''.join(child1_bin))
            child2_binaries.append(''.join(child2_bin))
        return (self.unit_factory.create_unit_with_binary_values(child1_binaries),
                self.unit_factory.create_unit_with_binary_values(child2_binaries))
