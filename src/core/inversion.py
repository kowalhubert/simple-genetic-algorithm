import random
from src.core.unit import Unit, UnitFactory

class StandardInversion:
    def __init__(self, unit_factory: UnitFactory, probability: int) -> None:
        assert probability is not None and 0 < probability < 100
        self.unit_factory = unit_factory
        self.probability = probability

    def invert(self, unit: Unit) -> Unit:
        """
        Invert a randomly chosen subsequence of the real-valued chromosome inside a Unit,
        with given probability (as a percentage 1-99).
        """
        # Probability check
        if random.random() >= self.probability / 100:
            return unit

        chromosome = unit.real_values.copy()
        length = len(chromosome)
        if length < 2:
            return unit

        # Choose random subsequence to invert
        left = random.randint(0, length - 2)
        right = random.randint(left + 1, length - 1)
        chromosome[left:right+1] = chromosome[left:right+1][::-1]

        return Unit(real_values=chromosome, cost=unit.cost)