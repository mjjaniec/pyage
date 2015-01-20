from unittest import TestCase

from pyage.solutions.evolution.crossover.permutation import PermutationCrossover, swaps_p1_to_p2


class TestPermutationCrossover(TestCase):
    @staticmethod
    def transform(p1, swaps):
        """:type p1: list of int
        :type swaps: list of (int, int)"""
        ret = list(p1)
        for (i, j) in swaps:
            ret[i], ret[j] = ret[j], ret[i]
        return ret

    def test_compute_difference_simple(self):
        pid = [0, 1, 2, 3, 4]
        pt1 = [0, 1, 3, 2, 4]
        pt2 = [0, 1, 4, 2, 3]
        pt3 = [1, 0, 4, 2, 3]

        d0 = swaps_p1_to_p2(pid, pid)
        self.assertListEqual(d0, [])

        d1 = swaps_p1_to_p2(pid, pt1)
        # one swap required
        self.assertEqual(len(d1), 1)
        # appalying difference to first list should yield second list
        self.assertListEqual(pt1, TestPermutationCrossover.transform(pid, d1))

        d2 = swaps_p1_to_p2(pid, pt2)
        self.assertEqual(len(d2), 2)
        self.assertListEqual(pt2, TestPermutationCrossover.transform(pid, d2))

        d3 = swaps_p1_to_p2(pid, pt3)
        self.assertEqual(len(d3), 3)
        self.assertListEqual(pt3, TestPermutationCrossover.transform(pid, d3))

    def test_compute_difference(self):
        p1 = [8, 0, 4, 6, 1, 3, 5, 7, 2]
        p2 = [4, 8, 0, 7, 5, 2, 6, 3, 1]
        p3 = [1, 7, 5, 6, 2, 8, 4, 0, 3]

        d0 = swaps_p1_to_p2(p1, p1)
        # difference between the same list should be empty
        self.assertListEqual(d0, [])

        d1 = swaps_p1_to_p2(p1, p2)
        # difference should be shorter than lists lengths
        self.assertLess(len(d1), len(p1))
        # appalying difference to first list should yield second list
        self.assertListEqual(p2, TestPermutationCrossover.transform(p1, d1))

        d2 = swaps_p1_to_p2(p2, p1)
        self.assertLess(len(d2), len(p1))
        self.assertListEqual(p1, TestPermutationCrossover.transform(p2, d2))

        d3 = swaps_p1_to_p2(p1, p3)
        self.assertLess(len(d3), len(p1))
        self.assertListEqual(p3, TestPermutationCrossover.transform(p1, d3))

        d4 = swaps_p1_to_p2(p3, p2)
        self.assertLess(len(d4), len(p1))
        self.assertListEqual(p2, TestPermutationCrossover.transform(p3, d4))









