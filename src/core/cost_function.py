from enum import Enum
import benchmark_functions as bf

class CostFunction(Enum):
    RASTRIGIN = ("Rastrigin", bf.Rastrigin)
    ROSENBROCK = ("Rosenbrock", bf.Rosenbrock)
    ACKLEY = ("Ackley", bf.Ackley)

    @property
    def name(self):
        return self.value[0]

    @property
    def func(self):
        return self.value[1]

