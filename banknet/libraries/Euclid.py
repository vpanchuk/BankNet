from math import sqrt
from functools import reduce

class Euclid:
    def distance(self, vector):
        return sqrt(reduce((lambda x, y: x+y), map(lambda x: x**2, vector)))