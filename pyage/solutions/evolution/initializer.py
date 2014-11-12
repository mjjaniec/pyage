from random import uniform
from pyage.core.emas import EmasAgent
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype, StringGenotype, PermutationGenotype
from pyage.utils import utils


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


class StringInitializer(Operator):
    def __init__(self, size=100):
        super(StringInitializer, self).__init__(StringGenotype)
        self.size = size

    def process(self, population):
        for i in xrange(self.size):
            population.append(StringGenotype(StringInitializer.gen_str()))

    @staticmethod
    def gen_str():
        length = randint(1, 10)
        result = ''
        for i in xrange(length):
            result += utils.rand_letter()
        return result


class PermutationInitializer(Operator):
    def __init__(self, length, size=100):
        """:type length: int"""
        super(PermutationInitializer, self).__init__(PermutationInitializer)
        self.size = size
        self.length = length

    def process(self, population):
        for _ in xrange(self.size):
            population.append(PermutationGenotype(PermutationInitializer.gen_permutation(self.length)))

    @staticmethod
    def gen_permutation(length):
        """ generate random permutation
        :type length: int
        :rtype: list of int"""
        ret = [i for i in xrange(length)]
        for i in xrange(length):
            j = randint(0, i)
            ret[i], ret[j] = ret[j], ret[i]
        return ret


def makota_agents_initializer(size, energy):
    agents = {}
    for i in xrange(size):
        agent = EmasAgent(StringGenotype(StringInitializer.gen_str()), energy)
        agents[agent.get_address()] = agent
    return agents

def float_emas_initializer(dims=2,energy=10, size=100, lowerbound=0.0, upperbound=1.0):
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

