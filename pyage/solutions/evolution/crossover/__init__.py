import random

from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype, StringGenotype
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


class UniformCrossover(AbstractCrossover):
    def __init__(self, size=100, probability=0.5):
        super(UniformCrossover, self).__init__(FloatGenotype, size)
        self.probability = probability

    def cross(self, p1, p2):
        return FloatGenotype([p1.genes[i] if random.random() < self.probability else p2.genes[i]
                              for i in range(len(p1.genes))])


# TODO(mjjaniec): Remove if unused
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