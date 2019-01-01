from .Vector import *
from .Matrix import *
from .Euclid import *
from copy import deepcopy

class KohonenNet(Vector, Matrix, Euclid):
          
    @property
    def ratio(self):
        return self.__ratio
        
    @ratio.setter
    def ratio(self, value):
        self.__ratio = value
        
    @property
    def iteration(self):
        return self.__iteration
        
    @iteration.setter
    def iteration(self, value):
        self.__iteration = value
        
    @property
    def method(self):
        return self.__method
        
    @method.setter
    def method(self, value):
        self.__method = value
        
    def era(self, points, weight, callable):
        return callable(points, weight)
        
    def solve(self, points, weight, ratio=None):
        self.iteration = 0
        w_prev = deepcopy(weight)
        weight_copy = deepcopy(weight)
        function = getattr(self, self.method)
        self.ratio = ratio if ratio else self.ratio
        self.era(points, weight_copy, function)
        while w_prev != weight_copy:
            w_prev = deepcopy(weight_copy)
            self.era(points, weight_copy, function)
            self.iteration += 1
            if self.iteration == 99:
                break
        return weight_copy

    def byEuclid(self, points, weight):
        lengthRow = len(points[0])
        lengthColumn = len(self.column(weight, 0))
        for j in range(lengthRow):
            temp, index = 0, 0
            minimum = self.distance([a_i-b_i for a_i, b_i in zip(self.column(points, j), self.column(weight, index))])
            for i in range(lengthColumn):
                temp = self.distance([a_i-b_i for a_i, b_i in zip(self.column(points, j), self.column(weight, i))])
                if temp < minimum:
                    minimum = temp
                    index = i
            for i in range(lengthColumn):
                weight[index][i] = weight[index][i] + self.ratio * (points[i][j]-weight[index][i])

    def byAngle(self, points, weight):
        lengthRow = len(points[0])
        lengthColumn = len(self.column(weight, 0))
        for j in range(lengthRow):
            i, temp, index, divider = 0, 0, 0, 0
            maximum = self.angle(self.column(points, j), self.column(weight, i))
            for i in range(lengthColumn):
                temp = self.angle(self.column(points, j), self.column(weight, i))
                if temp > maximum:
                    maximum = temp
                    index = i
            temp = self.module(self.column(weight, index))
            for i in range(lengthColumn):
                divider += (self.column(weight, index)[i] / temp + self.ratio * self.normalize(self.column(points, j))[i]) ** 2
            divider = sqrt(divider)
            for i in range(lengthColumn):
                weight[i][index] = (weight[i][index] / temp + self.ratio * self.normalize(self.column(points, j))[i]) / divider