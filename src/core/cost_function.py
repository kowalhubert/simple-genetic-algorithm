from enum import Enum
import benchmark_functions as bf
from opfunu.cec_based.cec2014 import F162014


class CEC2014_F16_Wrapper:
    def __init__(self, dimensions: int):
        # wymuszamy 30, bo tak działa oryginalna funkcja CEC2014
        self.func_obj = F162014()
        self.dimensions = 30  

    def __call__(self, x):
        return self.func_obj.evaluate(x)

    def suggested_bounds(self):
        return [-100] * self.dimensions, [100] * self.dimensions

class CostFunction(Enum):
    RASTRIGIN = ("Rastrigin", bf.Rastrigin)
    ROSENBROCK = ("Rosenbrock", bf.Rosenbrock)
    ACKLEY = ("Ackley", bf.Ackley)
    HYPERSHPERE = ("Hypersphere", bf.Hypersphere)
    CEC2014_F1 = ("CEC2014 - F16 Schwefel", CEC2014_F16_Wrapper)

    @property
    def name(self):
        return self.value[0]

    @property
    def func(self):
        return self.value[1]