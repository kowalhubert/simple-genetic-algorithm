from src.core.cost_function import CostFunction


class CostFunctionConfig:
    def __init__(self, dimensions: int, cost_function: CostFunction) -> None:
        assert dimensions > 0
        assert cost_function is not None
        self.dimensions = dimensions
        self.cost_func = cost_function.func(dimensions)