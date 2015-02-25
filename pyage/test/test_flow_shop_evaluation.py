from unittest import TestCase

from pyage.solutions.evolution.evaluation import FlowShopEvaluation


class TestFlowShopEvaluation(TestCase):
    def test_compute_fitness_1(self):
        time_matrix = [
            [1, 2, 5],
            [4, 5, 1],
            [5, 5, 3]
        ]
        evaluation = FlowShopEvaluation(time_matrix)

        expected_completion_times = [
            [1, 3, 8],
            [5, 10, 11],
            [10, 15, 18]
        ]
        makespan, completion_times = evaluation._compute_makespan([0, 1, 2], True)
        self.assertEqual(makespan, 18)
        self.assertListEqual(completion_times, expected_completion_times)

        self.assertEqual(evaluation._compute_makespan([0, 2, 1]), 18)
        self.assertEqual(evaluation._compute_makespan([1, 0, 2]), 20)
        expected_completion_times = [
            [2, 7, 8],
            [7, 8, 12],
            [12, 15, 20]
        ]
        makespan, completion_times = evaluation._compute_makespan([1, 2, 0], True)
        self.assertEqual(makespan, 20)
        self.assertListEqual(completion_times, expected_completion_times)
        self.assertEqual(evaluation._compute_makespan([2, 0, 1]), 20)
        self.assertEqual(evaluation._compute_makespan([2, 1, 0]), 22)

    def test_compute_fitness_2(self):
        time_matrix = [
            [1, 2, 3, 4, 5, 7],
            [2, 8, 4, 16, 4, 8],
            [3, 5, 9, 8, 2, 2],
            [12, 5, 2, 1, 4, 10]
        ]
        evaluation = FlowShopEvaluation(time_matrix)

        expected_completion_times = [
            [1, 3, 6, 10, 15, 22],
            [3, 11, 15, 31, 35, 43],
            [6, 16, 25, 39, 41, 45],
            [18, 23, 27, 40, 45, 55]
        ]
        makespan, completion_times = evaluation._compute_makespan(range(6), True)
        self.assertEqual(makespan, 55)
        self.assertListEqual(completion_times, expected_completion_times)

        expected_completion_times = [
            [5, 9, 16, 18, 21, 22],
            [9, 25, 33, 41, 45, 47],
            [11, 33, 35, 46, 55, 58],
            [15, 34, 45, 51, 57, 70]
        ]
        makespan, completion_times = evaluation._compute_makespan([4, 3, 5, 1, 2, 0], True)
        self.assertEqual(makespan, 70)
        self.assertListEqual(completion_times, expected_completion_times)
