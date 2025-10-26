import math
from typing import List


class Unit:
    def __init__(self, real_values: list[float], binary_values: list[float], cost: float = None) -> None:
        self.real_values = real_values
        self.binary_values = binary_values
        self.cost = cost

    def __repr__(self) -> str:
        return f"Unit(real_values={self.real_values}, binary_values={self.binary_values}, cost={self.cost})"
    

class UnitFactory:
    def __init__(self, lower_bound: float, upper_bound, precision: int) -> None:
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._accuracy = precision
        self._binary_length = self._calculate_binary_length()

    def _calculate_binary_length(self) -> int:
        n = (self._upper_bound - self._lower_bound) * (10 ** self._accuracy)
        return math.ceil(math.log2(n))
    
    def _real_to_binary(self, real_value: float) -> str:
        """Convert real value to binary string"""
        # Normalize to [0, 1] range
        normalized = (real_value - self._lower_bound) / (self._upper_bound - self._lower_bound)
        # Scale to integer
        scaled = int(normalized * (2**self._binary_length - 1))
        # Convert to binary
        binary = format(scaled, f'0{self._binary_length}b')
        return binary
    
    def _reals_to_binaries(self, real_values: list[float]) -> list[str]:
        return [self._real_to_binary(val) for val in real_values]

    def _binary_to_real(self, binary_string: str) -> float:
        """Convert binary string back to real value"""
        # Convert binary to integer
        integer_value = int(binary_string, 2)
        # Normalize to [0, 1] range
        normalized = integer_value / (2**self._binary_length - 1)
        # Scale back to original range
        real_value = self._lower_bound + normalized * (self._upper_bound - self._lower_bound)
        return real_value
    
    def _binaries_to_reals(self, binaries: list[str]) -> list[float]:
        """Convert binaries to list of decimal presentations"""
        return [self._binary_to_real(bin_val) for bin_val in binaries]

    def create_unit_with_real_values(self, real_values: list[float]) -> Unit:
        binary_values = self._reals_to_binaries(real_values)
        return Unit(real_values=real_values, binary_values=binary_values)

    def create_unit_with_binary_values(self, binary_values: list[str]) -> Unit:
        decimal_values = self._binaries_to_reals(binaries=binary_values)
        return Unit(real_values=decimal_values, binary_values=binary_values)
