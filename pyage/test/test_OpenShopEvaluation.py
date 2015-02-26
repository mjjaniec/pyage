from unittest import TestCase

from pyage.solutions.evolution.evaluation import OpenShopEvaluation


class TestOpenShopEvaluation(TestCase):
    time_matrix = [
        [1, 2, 5, 3],
        [4, 5, 1, 1],
        [5, 5, 3, 6]
    ]
    evaluation = OpenShopEvaluation(time_matrix)
    permutation = [5, 8, 2, 4, 11, 0, 1, 3, 9, 6, 7, 10]

    def test_compute_makespan(self):
        makespan = TestOpenShopEvaluation.evaluation.compute_makespan(TestOpenShopEvaluation.permutation)
        self.assertEqual(makespan, 29)

    def test_calculate_jobs_completion_times(self):
        expected = [18, 16, 28, 29]
        actual = TestOpenShopEvaluation.evaluation._calculate_jobs_completion_times(TestOpenShopEvaluation.permutation)
        self.assertEqual(expected, actual)
