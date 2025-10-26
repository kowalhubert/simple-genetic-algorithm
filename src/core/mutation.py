from src.core.unit import Unit, UnitFactory
from abc import ABC, abstractmethod
from enum import Enum
import random

class MutationMethodType(Enum):
    BOUNDARY = "Boundary"
    SINGLE_POINT = "Single-point"
    TWO_POINT = "Two-point"

class AbstractMutation(ABC):
    def __init__(self, probability: float, unit_factory: UnitFactory):
        self.probability = probability
        self.unit_factory = unit_factory

    @abstractmethod
    def mutate(self, unit: Unit) -> Unit:
        """
        Mutate a Unit and return a new Unit (with mutated real_values and binary_values).
        """
        pass

class BoundaryMutation(AbstractMutation):
    """
    Mutates a single gene in any dimension's binary chromosome to either all 0's or all 1's (min or max value for that dimension).
    """
    def mutate(self, unit: Unit) -> Unit:
        # Get the binary representation for all dimensions
        binaries = unit.binary_values
        mutated_binaries = []
        for i, binary in enumerate(binaries):
            bin_list = list(binary)
            for j in range(len(bin_list)):
                if random.random() < self.probability / 100:
                    # Set the bit string to boundary: either all 0s (min) or all 1s (max) with 50% chance
                    if random.random() < 0.5:
                        bin_list = ['0'] * len(bin_list)
                    else:
                        bin_list = ['1'] * len(bin_list)
                    break  # Only mutate one gene per dimension
            mutated_binaries.append("".join(bin_list))
        new_unit = self.unit_factory.create_unit_with_binary_values(mutated_binaries)
        new_unit.cost = unit.cost
        return new_unit

class SinglePointMutation(AbstractMutation):
    def mutate(self, unit: Unit) -> Unit:    
        binaries = unit.binary_values
        mutated_binaries = []
        for binary in binaries:
            if random.random() < self.probability / 100:
                length = len(binary)
                point = random.randint(0, length - 1)
                bin_list = list(binary)
                bin_list[point] = '0' if bin_list[point] == '1' else '1'
                mutated_binaries.append("".join(bin_list))
            else:
                mutated_binaries.append(binary)
        new_unit = self.unit_factory.create_unit_with_binary_values(mutated_binaries)
        new_unit.cost = unit.cost
        return new_unit

class TwoPointMutation(AbstractMutation):
    def mutate(self, unit: Unit) -> Unit:
        binaries = unit.binary_values
        mutated_binaries = []
        for binary in binaries:
            bin_list = list(binary)
            if random.random() < self.probability / 100:
                length = len(binary)
                if length < 2:
                    point1 = point2 = 0
                else:
                    point1, point2 = sorted(random.sample(range(length), 2))
                for i in range(point1, point2 + 1):
                    bin_list[i] = '0' if bin_list[i] == '1' else '1'
            mutated_binaries.append("".join(bin_list))
        new_unit = self.unit_factory.create_unit_with_binary_values(mutated_binaries)
        new_unit.cost = unit.cost
        return new_unit


