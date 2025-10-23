class GeneralConfig:
    def __init__(self, population_size: int, epochs_no: int, chromosome_repr_precistion: int) -> None:
        assert population_size > 0
        assert epochs_no > 0
        assert chromosome_repr_precistion > 0
        
        self.population_size = population_size
        self.epochs_no = epochs_no
        self.repr_precision = chromosome_repr_precistion