class Matrix:
    def transpose(self, matrix):
        return list(zip(*matrix))
    def column(self, matrix, i):
        return [row[i] for row in matrix]