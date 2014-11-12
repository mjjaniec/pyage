from math import cos, pi, sin, sqrt
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype, StringGenotype, PermutationGenotype

A = 10

class FloatRastriginEvaluation(Operator):
    def __init__(self):
        super(FloatRastriginEvaluation, self).__init__(FloatGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__rastrigin(genotype.genes)

    def __rastrigin(self, genes):
        sum = len(genes) * A
        for gene in genes:
            sum += gene ** 2 - A * cos(2 * pi * gene)
        return sum


class RastriginEvaluation(Operator):
    def __init__(self):
        super(RastriginEvaluation, self).__init__(PointGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__rastrigin(genotype.x, genotype.y)

    def __rastrigin(self, x, y):
        return 2 * A + x ** 2 - A * cos(2 * pi * x) + y ** 2 - A * cos(2 * pi * y)


class DeJongEvaluation(Operator):
    def __init__(self, type=None):
        super(DeJongEvaluation, self).__init__(PointGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__DeJong(genotype.x, genotype.y)

    def __DeJong(self, x, y):
        return x ** 2 + y ** 2


class SchwefelEvaluation(Operator):
    def __init__(self):
        super(SchwefelEvaluation, self).__init__()

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__schwefel(genotype.genes)

    def __schwefel(self, genes):
        sum = 418.9829
        for gene in genes:
            sum += -gene * sin(sqrt(abs(gene)))
        return sum


class MakotaEvaluation(Operator):
    def __init__(self):
        super(MakotaEvaluation, self).__init__(StringGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = 1.0 / (1.0 + MakotaEvaluation._distance("mama", genotype.genes))

    @staticmethod
    def _distance(s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        distances = range(len(s1) + 1)
        for index2, char2 in enumerate(s2):
            new_distance = [index2+1]
            for index1, char1 in enumerate(s1):
                if char1 == char2:
                    new_distance.append(distances[index1])
                else:
                    new_distance.append(1 + min((distances[index1],
                                                 distances[index1+1],
                                                 new_distance[-1])))
            distances = new_distance
        return distances[-1]


class FlowShopEvaluation(Operator):
    def __init__(self, time_matrix):
        """
        :type time_matrix: list of list
        :param time_matrix: time_matrix[processor][job]
        """
        super(FlowShopEvaluation, self).__init__(PermutationGenotype)
        self.time_matrix = time_matrix
        self.max_time = sum(sum(row) for row in time_matrix)

    def process(self, population):
        """ :type population: list of PermutationGenotype """
        for individual in population:
            individual.fitness = self.max_time - FlowShopEvaluation\
                .compute_makespan(individual.permutation)

    def compute_makespan(self, permutation, solution_matrix=None):
        """
        :param permutation: order of processing
        :type permutation: list of float
        :param time_matrix: time_matrix[processor][job]
        :type time_matrix: list of list
        :param solution_matrix: matrix - for solution
        :type solution_matrix: list of list
        :return: makespan for processing in given order (permutation)
        :rtype: float
        """

        back = []
        for i in xrange(len(self.time_matrix) + 1):
            back.append(0.0)
        for job in xrange(len(permutation)):
            for process in xrange(len(self.time_matrix)):
                back[process+1] = max(back[process+1], back[process]) + self.time_matrix[process][permutation[job]]
                if solution_matrix is not None:
                    solution_matrix[process][job] = back[process+1]

        return back[-1]


