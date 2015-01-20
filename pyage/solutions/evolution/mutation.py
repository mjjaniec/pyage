from copy import deepcopy
import random

from pyage.core.inject import Inject
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype, PermutationGenotype


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


class NormalMutation(object):
    def __init__(self, probability=0.01, radius=0.1):
        super(NormalMutation, self).__init__()
        self.probability = probability
        self.radius = radius

    def mutate(self, genotype):
        for index in range(len(genotype.genes)):
            if random.random() < self.probability:
                genotype.genes[index] = random.gauss(genotype.genes[index], self.radius)


class PermutationMutation(AbstractMutation):
    def __init__(self, random_swaps_count, probability=0.4):
        """:param random_swaps_count: int"""
        super(PermutationMutation, self).__init__(PermutationGenotype, probability)
        self.random_swaps_count = random_swaps_count

    def mutate(self, genotype):
        """:type genotype: PermutationGenotype"""

        def perform_random_swap(permutation):
            """ :param permutation: list of int """
            length = len(permutation)
            i = random.randint(0, length - 1)
            j = random.randint(0, length - 1)
            permutation[i], permutation[j] = permutation[j], permutation[i]

        for _ in xrange(self.random_swaps_count):
            perform_random_swap(genotype.permutation)


class MemeticPermutationMutation(PermutationMutation):
    def __init__(self, local_rounds_count, attempts_per_round, random_swaps_count, probability=0.4):
        """:param random_swaps_count: int
           :param random_swaps_count: int"""
        super(MemeticPermutationMutation, self).__init__(random_swaps_count, probability)
        self.local_rounds_count = local_rounds_count
        self.attempts_per_round = attempts_per_round

    @Inject('evaluation')
    def mutate(self, genotype):
        """:type genotype: PermutationGenotype"""

        def fitness(genotype):
            result = self.evaluation.compute_makespan(genotype.permutation)
            return result

        def do_round():
            def perform_mutation(round_base_genotype):
                candidate_genotype = deepcopy(round_base_genotype)
                super(MemeticPermutationMutation, self).mutate(candidate_genotype)
                candidate_fitness = fitness(candidate_genotype)
                return candidate_fitness, candidate_genotype

            def update_best_if_better(candidate_fitness, candidate_genotype):
                if candidate_fitness < best['fitness']:
                    best['genotype'] = candidate_genotype
                    best['fitness'] = candidate_fitness

            round_base_genotype = deepcopy(best['genotype'])
            for _ in xrange(self.attempts_per_round):
                candidate_fitness, candidate_genotype = perform_mutation(round_base_genotype)
                update_best_if_better(candidate_fitness, candidate_genotype)

        best = {'genotype': genotype, 'fitness': fitness(genotype)}  # why a map? here: http://stackoverflow.com/a/2609593/1432478
        for _ in xrange(self.local_rounds_count):
            do_round()
        genotype.permutation = best['genotype'].permutation  # genotype = best_genotype won't work
