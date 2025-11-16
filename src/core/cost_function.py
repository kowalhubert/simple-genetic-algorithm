from enum import Enum
import benchmark_functions as bf
from opfunu.cec_based.cec2014 import F32014


class CEC2014_F3_Wrapper:
    def __init__(self, dimensions: int):
        self.dimensions = dimensions
        self.func_obj = F32014(ndim=dimensions)

    def __call__(self, x):
        return self.func_obj.evaluate(x)

    def suggested_bounds(self):
        return [-100] * self.dimensions, [100] * self.dimensions


class CostFunction(Enum):
    RASTRIGIN = ("Rastrigin", bf.Rastrigin)
    ROSENBROCK = ("Rosenbrock", bf.Rosenbrock)
    ACKLEY = ("Ackley", bf.Ackley)
    HYPERSPHERE = ("Hypersphere", bf.Hypersphere)
    HYPERELLIPSOID = ("Hyperellipsoid", bf.Hyperellipsoid)
    CEC2014_F3 = ("CEC2014 - F3 Shifted Rotated High Conditioned Elliptic Function", CEC2014_F3_Wrapper)

    @property
    def name(self):
        return self.value[0]

    @property
    def func_class(self):
        return self.value[1]