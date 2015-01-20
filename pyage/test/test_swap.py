from unittest import TestCase

from pyage.solutions.evolution.crossover.permutation import swap


class Test_swap(TestCase):
    def test_swap(self):
        a = ['magnets beyotch']
        e = ['magnets beyotch']  # e - expected. Lame name, to keep the assignments aligned
        swap(a, 0, 0)
        self.assertListEqual(e, a)

        a = ['magnets beyotch', 'the danger']
        e = ['magnets beyotch', 'the danger']
        swap(a, 1, 1)
        self.assertListEqual(e, a)

        a = [1, 2, 3, 4, 5]
        e = [1, 4, 3, 2, 5]
        swap(a, 1, 3)
        self.assertListEqual(e, a)
