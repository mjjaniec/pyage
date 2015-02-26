from unittest import TestCase

from pyage.solutions.evolution.crossover.permutation import FirstHalfSwapsCrossover
from pyage.solutions.evolution.genotype import PermutationGenotype


class TestFirstHalfSwapsCrossover(TestCase):
    def test_first_half(self):
        a = []
        expected = []
        actual = FirstHalfSwapsCrossover._first_half(a)
        self.assertListEqual(expected, actual)

        a = [1]
        expected = []
        actual = FirstHalfSwapsCrossover._first_half(a)
        self.assertListEqual(expected, actual)

        a = [2, 5]
        expected = [2]
        actual = FirstHalfSwapsCrossover._first_half(a)
        self.assertListEqual(expected, actual)

        a = [10, 1, 100]
        expected = [10]
        actual = FirstHalfSwapsCrossover._first_half(a)
        self.assertListEqual(expected, actual)

        a = [10, 1, 100, 2, 3, 600]
        expected = [10, 1, 100]
        actual = FirstHalfSwapsCrossover._first_half(a)
        self.assertListEqual(expected, actual)

    def test_cross(self):
        pi = PermutationGenotype([1, 2, 3, 4, 5, 6, 7])
        p1 = PermutationGenotype([2, 3, 5, 1, 4, 7, 6])
        # swaps: [(0, 1), (1, 2), (2, 4), (4, 3), (5, 6)]
        expected = PermutationGenotype([2, 3, 1, 4, 5, 6, 7])
        actual = FirstHalfSwapsCrossover().cross(pi, p1)
        self.assertEqual(expected.permutation, actual.permutation)

        pi = PermutationGenotype([1, 2, 3, 4, 5, 6])
        p1 = PermutationGenotype([2, 3, 5, 1, 4, 6])
        # swaps: [(0, 1), (1, 2), (2, 4), (4, 3)]
        expected = PermutationGenotype([2, 3, 1, 4, 5, 6])
        actual = FirstHalfSwapsCrossover().cross(pi, p1)
        self.assertEqual(expected.permutation, actual.permutation)
