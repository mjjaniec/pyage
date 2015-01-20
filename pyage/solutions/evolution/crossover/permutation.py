from pyage.solutions.evolution.crossover import AbstractCrossover
from pyage.solutions.evolution.genotype import PermutationGenotype
from pyage.utils import utils


class PermutationCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(PermutationCrossover, self).__init__(PermutationGenotype, size)

    def cross(self, p1, p2):
        """
        :type p1: PermutationGenotype
        :type p2: PermutationGenotype
        :rtype PermutationGenotype"""

        difference = PermutationCrossover.compute_difference(p1.permutation, p2.permutation)
        offspring = PermutationGenotype(list(p1.permutation))

        # execute about a half of transformation from p1, to p2
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

        result = []
        visited = [False] * len(p1)
        position_in_p1 = {p1[i]: i for i in range(len(p1))}

        for i in xrange(len(p1)):
            if not visited[i]:  # start a cycle
                while not visited[i]:
                    visited[i] = True
                    next = position_in_p1[p2[i]]
                    result.append((i, next))
                    i = next
                # last element is not necessary (forced by previous entries)
                result.pop()
        return result