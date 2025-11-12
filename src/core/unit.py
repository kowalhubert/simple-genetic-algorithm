from typing import List
import random

class Unit:
    def __init__(self, real_values: List[float], cost: float = None) -> None:
        self.real_values = real_values
        self.cost = cost

    def __repr__(self) -> str:
        return f"Unit(real_values={self.real_values}, cost={self.cost})"


class UnitFactory:
    def __init__(self, lower_bound: float, upper_bound: float) -> None:
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

    def create_random_unit(self, dimension: int) -> Unit:
        """Generate a random unit with 'dimension' real values within bounds"""
        real_values = [random.uniform(self._lower_bound, self._upper_bound) for _ in range(dimension)]
        return Unit(real_values=real_values)