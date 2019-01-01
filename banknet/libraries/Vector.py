from math import sqrt
from functools import reduce

class Vector:
    def module(self, vector):
        return sqrt(reduce((lambda x, y: x+y), map(lambda x: x**2, vector)))
    def multiplication(self, vector_a, vector_b):
        return reduce((lambda x, y: x+y), map(lambda x, y: x*y, vector_a, vector_b))
    def angle(self, vector_a, vector_b):
        return self.multiplication(vector_a, vector_b)/(self.module(vector_a) * self.module(vector_b))
    def normalize(self, vector):
        length = self.module(vector)
        return list(map(lambda x: x/length, vector))