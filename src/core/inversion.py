import random
from src.core.unit import Unit, UnitFactory

class StandardInversion:
    def __init__(self, unit_factory: UnitFactory,  probability: int) -> None:
        assert probability is not None and probability > 0 and probability < 100
        self.unit_factory = unit_factory
        self.probability = probability

    def invert(self, unit: Unit) -> Unit:
        """
        Invert a randomly chosen subsequence of the real-valued chromosome inside a Unit,
        with given probability (as a percentage 1-99).
        Assumes 'unit' is an instance of Unit, and uses its binary_values representation.

        Returns a new Unit with inverted chromosome, or a (deep) copy if not inverted.
        """
        # Probability check (convert % to [0,1])
        if random.random() >= self.probability / 100:
            return unit
        
        chromosome = unit.binary_values.copy()
        full_bits = ''.join(chromosome)
        length = len(full_bits)
        if length < 2:
            return unit

        left = random.randint(0, length - 2)
        right = random.randint(left + 1, length - 1)
        inverted_bits = (
            full_bits[:left]
            + full_bits[left:right+1][::-1]
            + full_bits[right+1:]
        )

        # Re-chop into the original bit string layouts
        dims = [len(b) for b in chromosome]
        result = []
        i = 0
        for dlen in dims:
            result.append(inverted_bits[i:i+dlen])
            i += dlen

        return self.unit_factory.create_unit_with_binary_values(result)
