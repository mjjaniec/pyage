from unittest import TestCase
from pyage.solutions.evolution.evaluation import FlowShopEvaluation


class TestFlowShopEvaluation(TestCase):
    time_matrix = [
        [1, 2, 5],
        [4, 5, 1],
        [5, 5, 3]
    ]

    time_table = [
        [1, 3, 8],
        [5, 10, 11],
        [10, 15, 18]
    ]

    def test_compute_fitness(self):
        evaluation = FlowShopEvaluation(TestFlowShopEvaluation.time_matrix)
        self.assertEqual(evaluation.compute_makespan([0, 1, 2]), 18)
        self.assertEqual(evaluation.compute_makespan([0, 2, 1]), 18)
        self.assertEqual(evaluation.compute_makespan([1, 2, 0]), 20)
        self.assertEqual(evaluation.compute_makespan([1, 0, 2]), 20)
        self.assertEqual(evaluation.compute_makespan([2, 0, 1]), 20)
        self.assertEqual(evaluation.compute_makespan([2, 1, 0]), 22)

    def test_compute_time_table(self):
        evaluation = FlowShopEvaluation(TestFlowShopEvaluation.time_matrix)
        makespan, result_table = evaluation.compute_makespan([0, 1, 2], True)
        self.assertEqual(makespan, 18)
        self.assertListEqual(result_table, TestFlowShopEvaluation.time_table)
