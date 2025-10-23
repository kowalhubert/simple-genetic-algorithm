from abc import ABC, abstractmethod
from enum import Enum
import random

# Implementacja metod selekcji najlepszych, kołem ruletki, selekcji turniejowej +
# konfiguracje parametrów

class SelectionMethodType(Enum):
    BEST = "Best"
    ROULETTE = "Roulette Wheel"
    TOURNAMENT = "Tournament"


class SelectionMethod(ABC):
    @abstractmethod
    def select(self, population, num):
        """Select individuals from the population."""
        pass

class BestSelection(SelectionMethod):
    def select(self, population, num):
        # Select the top 'num' individuals based on highest fitness
        return sorted(population, key=lambda ind: ind.fitness, reverse=True)[:num]

class RouletteWheelSelection(SelectionMethod):
    def select(self, population, num):
        # Select 'num' individuals using roulette wheel (fitness-proportional) selection
        fitness_sum = sum(ind.fitness for ind in population)
        if fitness_sum == 0:
            # If all fitness values are 0, fall back to random selection
            return random.sample(population, num)
        selected = []
        for _ in range(num):
            pick = random.uniform(0, fitness_sum)
            current = 0
            for ind in population:
                current += ind.fitness
                if current >= pick:
                    selected.append(ind)
                    break
        return selected

class TournamentSelection(SelectionMethod):
    def __init__(self, tournament_size=3):
        self.tournament_size = tournament_size

    def select(self, population, num):
        # Select 'num' individuals using tournament selection
        selected = []
        for _ in range(num):
            contenders = random.sample(population, min(self.tournament_size, len(population)))
            winner = max(contenders, key=lambda ind: ind.fitness)
            selected.append(winner)
        return selected
