
from src.core.inversion import StandardInversion
from src.core.unit import UnitFactory


class InversionConfig:
    def __init__(self, unit_factory: UnitFactory, probability: int):
        assert probability is not None and probability > 0 and probability < 100
        self.__probability = probability
        self.inversion_func = StandardInversion(unit_factory, probability).invert
        
        # Public property for serialization
        self.probability = probability 