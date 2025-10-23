
from src.core.inversion import StandardInversion


class InversionConfig:
    def __init__(self, probability: int):
        assert probability is not None and probability > 0 and probability < 100
        self.__probability = probability
        self.inversion_func = StandardInversion(probability).invert 