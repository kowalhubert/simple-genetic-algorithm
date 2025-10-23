from typing import List

class EliteStrategy:
    """
    Implements the elitism operator for evolutionary algorithms.
    Keeps the top N elite individuals unchanged to the next generation.
    """

    def __init__(self, elite_count: int):
        assert elite_count is not None and elite_count >= 0, "elite_count must be non-negative integer"
        self.elite_count = elite_count

    def select_elite(self, population: List, fitness: List[float]) -> List:
        """
        Return the top `elite_count` individuals from the population based on fitness.
        
        Args:
            population: List of individuals (chromosomes).
            fitness: List of fitness values (ordered same as population, higher is better).
        
        Returns:
            List of elite individuals (length=min(elite_count, len(population)))
        """
        assert len(population) == len(fitness), "Population and fitness must have the same length"
        if self.elite_count == 0 or not population:
            return []

        # Pair individuals with their fitness and sort descending by fitness
        indexed = list(enumerate(fitness))
        # Assuming higher fitness is better; reverse=True
        elite_indices = sorted(indexed, key=lambda x: x[1], reverse=True)[:self.elite_count]
        elite_individuals = [population[i] for i, _ in elite_indices]
        return elite_individuals
