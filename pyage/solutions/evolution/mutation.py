import random
from pyage.utils import utils
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype, StringGenotype, PermutationGenotype


class AbstractMutation(Operator):
    def __init__(self, type, probability):
        super(AbstractMutation, self).__init__()
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.mutate(genotype)


class UniformPointMutation(AbstractMutation):
    def __init__(self, probability=0.1, radius=100.5):
        super(UniformPointMutation, self).__init__(PointGenotype, probability)
        self.radius = radius

    def mutate(self, genotype):
        genotype.x = genotype.x + random.uniform(-self.radius, self.radius)
        genotype.y = genotype.y + random.uniform(-self.radius, self.radius)


class UniformFloatMutation(AbstractMutation):
    def __init__(self, probability=0.1, radius=0.5):
        super(UniformFloatMutation, self).__init__(FloatGenotype, probability)
        self.radius = radius

    def mutate(self, genotype):
        index = random.randint(0, len(genotype.genes) - 1)
        genotype.genes[index] += random.uniform(-self.radius, self.radius)


class StringMutation(AbstractMutation):
    def __init__(self, probability=0.1):
        super(StringMutation, self).__init__(StringGenotype, probability)

    def mutate(self, genotype):
        new_genes = StringMutation.do_mutate(genotype.genes)
        genotype.genes = new_genes

    @staticmethod
    def do_mutate(string):
        index = random.randint(0, len(string) -1)
        if random.random() < 0.6:
            # change one letter
            return string[:index] + utils.rand_letter() + string[index+1:]
        elif random.random() < 0.5 and len(string) > 1:
            # remove one letter
            return string[:index] + string[index+1:]
        else:
            # add one letter
            return string[:index] + utils.rand_letter() + string[index:]


class PermutationMutation(AbstractMutation):
    def __init__(self, count, probability=0.4):
        """:param count: int"""
        super(PermutationMutation, self).__init__(PermutationGenotype, probability)
        self.count = count

    def mutate(self, genotype):
        """:type genotype: PermutationGenotype"""
        for _ in xrange(self.count):
            PermutationMutation.do_mutate(genotype.permutation)

    @staticmethod
    def do_mutate(permutation):
        """ :param permutation: list of int """
        length = len(permutation)
        i = random.randint(0, length)
        j = random.randint(0, length)
        permutation[i], permutation[j] = permutation[j], permutation[j]






