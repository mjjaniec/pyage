from unittest import TestCase
from pyage.solutions.evolution.genotype import PermutationGenotype
from pyage.solutions.evolution.evaluation import FlowShopEvaluation
from pyage.solutions.evolution.crossover import PermutationCrossover, AverageFloatCrossover
from pyage.solutions.evolution.mutation import PermutationMutation
import serpent

__author__ = 'mjjaniec'


class TestSerialization(TestCase):
    def setUp(self):
        self.ser = serpent.Serializer()

    def test_genotype_serialization(self):
        ls = [1, 5, 2, 4, 3]
        data = self.ser.serialize(PermutationGenotype(ls))
        self.assertListEqual(ls, serpent.loads(data)['permutation'])

    def test_evaluation_serialization(self):
        evaluation = FlowShopEvaluation([[1, 2, 3], [4, 5, 6]])
        data = self.ser.serialize(evaluation)
        serpent.loads(data)

    def test_mutation_serialization(self):
        mutation = PermutationMutation(1)
        data = self.ser.serialize(mutation)
        serpent.loads(data)

    def test_crossover_serialization(self):
        crossover = PermutationCrossover()
        data = self.ser.serialize(crossover)
        serpent.loads(data)