import random
from random import uniform

from pyage.core.emas import EmasAgent
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype, PermutationGenotype


class PointInitializer(Operator):
    def __init__(self, size=100, lowerbound=0.0, upperbound=1.0):
        super(PointInitializer, self).__init__(PointGenotype)
        self.size = size
        self.lowerbound = lowerbound
        self.upperbound = upperbound

    def process(self, population):
        for i in range(self.size):
            population.append(PointGenotype(self.__randomize(), self.__randomize()))

    def __randomize(self):
        return uniform(self.lowerbound, self.upperbound)


class FloatInitializer(Operator):
    def __init__(self, dims=3, size=100, lowerbound=0.0, upperbound=1.0):
        super(FloatInitializer, self).__init__(FloatGenotype)
        self.size = size
        self.lowerbound = lowerbound
        self.upperbound = upperbound
        self.dims = dims

    def process(self, population):
        for i in range(self.size):
            population.append(FloatGenotype([self.__randomize() for _ in range(self.dims)]))

    def __randomize(self):
        return uniform(self.lowerbound, self.upperbound)


class PermutationInitializer(Operator):
    def __init__(self, permutation_length, population_size=100):
        super(PermutationInitializer, self).__init__(PermutationGenotype)
        self.permutation_length = permutation_length
        self.population_size = population_size

    def process(self, population):
        for _ in xrange(self.population_size):
            population.append(PermutationGenotype(PermutationInitializer.generate_permutation(self.permutation_length)))

    @staticmethod
    def generate_permutation(permutation_length):
        permutation = range(permutation_length)
        random.shuffle(permutation)
        return permutation


def flowshop_agents_initializer(size, length, energy):
    agents = {}
    for i in xrange(size):
        agent = EmasAgent(PermutationGenotype(PermutationInitializer.generate_permutation(length)), energy)
        agents[agent.get_address()] = agent
    return agents


def float_emas_initializer(dims=2, energy=10, size=100, lowerbound=0.0, upperbound=1.0):
    agents = {}
    for i in range(size):
        agent = EmasAgent(FloatGenotype([uniform(lowerbound, upperbound) for _ in range(dims)]), energy)
        agents[agent.get_address()] = agent
    return agents


def emas_initializer(energy=10, size=100, lowerbound=0.0, upperbound=1.0):
    agents = {}
    for i in range(size):
        agent = EmasAgent(PointGenotype(uniform(lowerbound, upperbound), uniform(lowerbound, upperbound)), energy)
        agents[agent.get_address()] = agent
    return agents
