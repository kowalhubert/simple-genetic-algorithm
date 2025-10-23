from abc import ABC, abstractmethod
from enum import Enum
import random

class MutationMethodType(Enum):
    BOUNDARY = "Boundary"
    SINGLE_POINT = "Single-point"
    TWO_POINT = "Two-point"

class AbstractMutation(ABC):
    def __init__(self, probability: float):
        self.probability = probability

    @abstractmethod
    def mutate(self, chromosome: list, min_value: int, max_value: int) -> list:
        pass

class BoundaryMutation(AbstractMutation):
    """
    Mutates a single gene to either the minimum or maximum allowed value (randomly chosen).
    """
    def mutate(self, chromosome: list, min_value: int, max_value: int) -> list:
        mutated = chromosome.copy()
        for i in range(len(mutated)):
            if random.random() < self.probability:
                mutated[i] = random.choice([min_value, max_value])
        return mutated

class SinglePointMutation(AbstractMutation):
    """
    Mutates a single, randomly chosen gene of the chromosome to a random value in [min_value, max_value].
    """
    def mutate(self, chromosome: list, min_value: int, max_value: int) -> list:
        mutated = chromosome.copy()
        if random.random() < self.probability:
            idx = random.randint(0, len(mutated) - 1)
            mutated[idx] = random.randint(min_value, max_value)
        return mutated

class TwoPointMutation(AbstractMutation):
    """
    Mutates two (possibly same) randomly chosen genes of the chromosome to random values in [min_value, max_value].
    """
    def mutate(self, chromosome: list, min_value: int, max_value: int) -> list:
        mutated = chromosome.copy()
        for _ in range(2):
            if random.random() < self.probability:
                idx = random.randint(0, len(mutated) - 1)
                mutated[idx] = random.randint(min_value, max_value)
        return mutated
