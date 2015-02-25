from unittest import TestCase

from pyage.solutions.evolution.crossover.permutation import first_half


class Test_first_half(TestCase):
    def test_first_half(self):
        a = []
        expected = []
        actual = first_half(a)
        self.assertListEqual(expected, actual)

        a = [1]
        expected = []
        actual = first_half(a)
        self.assertListEqual(expected, actual)

        a = [2, 5]
        expected = [2]
        actual = first_half(a)
        self.assertListEqual(expected, actual)

        a = [10, 1, 100]
        expected = [10]
        actual = first_half(a)
        self.assertListEqual(expected, actual)

        a = [10, 1, 100, 2, 3, 600]
        expected = [10, 1, 100]
        actual = first_half(a)
        self.assertListEqual(expected, actual)
