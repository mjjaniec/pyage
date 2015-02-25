from unittest import TestCase

from pyage.solutions.evolution.crossover.permutation import swap


class Test_swap(TestCase):
    def test_swap(self):
        actual = ['magnets beyotch']
        expected = ['magnets beyotch']
        swap(actual, 0, 0)
        self.assertListEqual(expected, actual)

        actual = ['magnets beyotch', 'the danger']
        expected = ['magnets beyotch', 'the danger']
        swap(actual, 1, 1)
        self.assertListEqual(expected, actual)

        actual = [1, 2, 3, 4, 5]
        expected = [1, 4, 3, 2, 5]
        swap(actual, 1, 3)
        self.assertListEqual(expected, actual)
