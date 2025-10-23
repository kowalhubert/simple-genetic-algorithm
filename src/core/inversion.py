from abc import ABC, abstractmethod
import random
from enum import Enum

class StandardInversion:
    def __init__(self, probability: int) -> None:
        assert probability is not None and probability > 0 and probability < 100
        self.probability = probability
    """
    Inverts a randomly chosen subsequence of the chromosome with probability.
    """
    def invert(self, chromosome: list) -> list:
        if random.random() >= self.probability:
            return chromosome.copy()
        length = len(chromosome)
        if length < 2:
            return chromosome.copy()

        left = random.randint(0, length - 2)
        right = random.randint(left + 1, length - 1)
        inverted = chromosome.copy()
        inverted[left:right+1] = reversed(inverted[left:right+1])
        return inverted
