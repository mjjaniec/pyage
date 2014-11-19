import random
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype, StringGenotype, PermutationGenotype
from pyage.utils import utils


class AbstractCrossover(Operator):
    def __init__(self, type, size):
        super(AbstractCrossover, self).__init__(type)
        self.__size = size

    def process(self, population):
        parents = list(population)
        for i in range(len(population), self.__size):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)


class AverageCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(AverageCrossover, self).__init__(PointGenotype, size)

    def cross(self, p1, p2):
        genotype = PointGenotype((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)
        return genotype


class AverageFloatCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(AverageFloatCrossover, self).__init__(FloatGenotype, size)

    def cross(self, p1, p2):
        genotype = FloatGenotype([sum(p) / 2.0 for p in zip(p1.genes, p2.genes)])
        return genotype

class SinglePointCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(SinglePointCrossover, self).__init__(FloatGenotype, size)


    def cross(self, p1, p2):
        crossingPoint = random.randint(1, len(p1.genes))
        return FloatGenotype(p1.genes[:crossingPoint] + p2.genes[crossingPoint:])


class PermutationCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(PermutationCrossover, self).__init__(PermutationGenotype.__name__, size)

    def cross(self, p1, p2):
        """
        :type p1: PermutationGenotype
        :type p2: PermutationGenotype
        :rtype PermutationGenotype"""

        difference = PermutationCrossover.compute_difference(p1.permutation, p2.permutation)
        offspring = PermutationGenotype(list(p1.permutation))

        #execute about a half of transformation from p1, to p2
        for (i, j) in difference:
            if utils.rand_bool():
                offspring.permutation[i], offspring.permutation[j] = offspring.permutation[j], offspring.permutation[i]

        # p1o = PermutationCrossover.compute_difference(p1.permutation, offspring.permutation)
        # p2o = PermutationCrossover.compute_difference(p2.permutation, offspring.permutation)
        # print (len(difference), len(p1o), len(p2o))
        return offspring

    @staticmethod
    def compute_difference(p1, p2):
        """
        :type p1: list of int
        :type  p2: list of int
        :rtype: list of (int, int)
        :return: minimal list of swaps necessary to transform p1 into p2
        """

        ret = []
        visited = [False] * len(p1)
        reversed = [None] * len(p1)

        for i in xrange(len(p1)):
            reversed[p1[i]] = i

        for i in xrange(len(p1)):
            if not visited[i]:  # start a cycle
                prev = i
                while not visited[i]:
                    visited[i] = True
                    i = reversed[p2[i]]
                    ret.append((prev, i))
                    prev = i
                #last element is not necessary (forced by previous entries)
                ret.pop()
        return ret


class StringCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(StringCrossover, self).__init__(StringGenotype, size)

    def cross(self, p1, p2):
        if utils.rand_bool():
            p1, p2 = p2, p1

        result = []
        len1 = len(p1.genes)
        len2 = len(p2.genes)
        len_both = len1 + len2
        i1 = 0
        i2 = 0
        for i in xrange(len_both):
            fi = float(i)
            while float(i1) / len1 <= fi / len_both:
                if utils.rand_bool():
                    result.append(p1.genes[i1])
                i1 += 1
            while float(i2) / len2 <= fi / len_both:
                if utils.rand_bool():
                    result.append(p2.genes[i2])
                i2 += 1

        while i1 < len1:
            if utils.rand_bool():
                result.append(p1.genes[i1])
            i1 += 1
        while i2 < len2:
            if utils.rand_bool():
                result.append(p2.genes[i2])
            i2 += 2

        if len(result) == 0:
            result.append(utils.rand_letter())

        return StringGenotype(''.join(result))