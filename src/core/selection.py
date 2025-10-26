from abc import ABC, abstractmethod
from enum import Enum
import random
from typing import List

from src.core.unit import Unit


class SelectionMethodType(Enum):
    BEST = "Best"
    ROULETTE = "Roulette Wheel"
    TOURNAMENT = "Tournament"

class SelectionMethod(ABC):
    def __init__(self, is_maximization: bool = True) -> None:
        self._is_maximization = is_maximization

    @abstractmethod
    def select(self, population, num) -> List[Unit]:
        """Select individuals from the population."""
        pass

class BestSelection(SelectionMethod):
    def select(self, population, num):
        return sorted(population, key=lambda ind: ind.cost, reverse=self._is_maximization)[:num]

class RouletteWheelSelection(SelectionMethod):
    def select(self, population, num):
        if self._is_maximization:
            scores = [ind.cost for ind in population]
        else:
            # For minimization, flip costs to convert to maximization on [costs]
            max_cost = max(ind.cost for ind in population)
            min_cost = min(ind.cost for ind in population)
            # Prevent negative or zero weights, add small epsilon if needed
            if max_cost == min_cost:
                scores = [1.0 for _ in population]
            else:
                scores = [max_cost - ind.cost + 1e-9 for ind in population]
        total_score = sum(scores)
        if total_score == 0:
            return random.sample(population, num)
        selected = []
        for _ in range(num):
            pick = random.uniform(0, total_score)
            current = 0
            for ind, score in zip(population, scores):
                current += score
                if current >= pick:
                    selected.append(ind)
                    break
        return selected

class TournamentSelection(SelectionMethod):
    def __init__(self, tournament_size=3, is_maximization: bool = True):
        super().__init__(is_maximization)
        self.tournament_size = tournament_size

    def select(self, population, num):
        population_pool = population[:]
        selected = []
        
        tournaments_count = len(population) // self.tournament_size
        plus_one = 1 if len(population) % self.tournament_size > 0 else 0
        tournaments_count += plus_one

        while len(selected) < tournaments_count and population_pool:
            k = min(self.tournament_size, len(population_pool))
            contenders = random.sample(population_pool, k)
            if self._is_maximization:
                winner = max(contenders, key=lambda ind: ind.cost)
            else:
                winner = min(contenders, key=lambda ind: ind.cost)
            selected.append(winner)
            population_pool.remove(winner)
        return selected
