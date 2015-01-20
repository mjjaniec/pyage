from pyage.solutions.evolution.crossover import AbstractCrossover
from pyage.solutions.evolution.genotype import PermutationGenotype
from pyage.utils import utils


def swaps_p1_to_p2(p1, p2):
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
                next_ = position_in_p1[p2[i]]
                result.append((i, next_))
                i = next_
            result.pop()  # last swap is excessive
    return result


def swap(list_, i, j):
    list_[i], list_[j] = list_[j], list_[i]


class DummyHalfSwapsCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(DummyHalfSwapsCrossover, self).__init__(PermutationGenotype, size)

    def cross(self, p1, p2):
        """
        :type p1: PermutationGenotype
        :type p2: PermutationGenotype
        :rtype PermutationGenotype"""

        genotype = PermutationGenotype(list(p1.permutation))
        swaps = swaps_p1_to_p2(p1.permutation, p2.permutation)

        # execute a half (statistically!) of swaps from p1, to p2 - hence Dummy
        for (i, j) in swaps:
            if utils.rand_bool():
                swap(genotype.permutation, i, j)

        return genotype


def first_half(list_):
    return list_[:len(list_) // 2]


class FirstHalfSwapsCrossover(AbstractCrossover):
    def __init__(self, size=100):
        super(FirstHalfSwapsCrossover, self).__init__(PermutationGenotype, size)

    def cross(self, p1, p2):
        """
        :type p1: PermutationGenotype
        :type p2: PermutationGenotype
        :rtype PermutationGenotype"""

        swaps = swaps_p1_to_p2(p1.permutation, p2.permutation)
        genotype = PermutationGenotype(list(p1.permutation))

        # execute first half of swaps from p1, to p2
        for (i, j) in first_half(swaps):
            swap(genotype.permutation, i, j)

        # TODO(vucalur): should return 2 children: from first and second half on the swaps.
        # TODO(vucalur): modify AbstractCrossover so it can handle such usage
        return genotype