import math
        

class Chromosome:
    def __init__(self, lower_bound, upper_bound, accuracy) -> None:
        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
        self.__accuracy = accuracy
        self.binary_representation = self.__generate_binary_representation()

    def __generate_binary_representation(self):
        n = (self.__upper_bound - self.__lower_bound) * (10 ** self.__accuracy)
        return math.ceil(math.log2(n))
