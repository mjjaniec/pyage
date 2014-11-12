# coding=utf-8
import logging
import time

from pyage.core import address

from pyage.core.agent.agent import unnamed_agents
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import GridLocator
from pyage.core.migration import ParentMigration
from pyage.core.stats.statistics import WithGenomeStatistics
from pyage.core.stop_condition import StepLimitStopCondition, TimeLimitStopCondition
from pyage.solutions.evolution.crossover import PermutationCrossover
from pyage.solutions.evolution.evaluation import FlowShopEvaluation
from pyage.solutions.evolution.initializer import flow_shop_agents_initializer, PermutationInitializer
from pyage.solutions.evolution.mutation import PermutationMutation

time_matrix = [
    [54, 83, 15, 71, 77, 36, 53, 38, 27, 87, 76, 91, 14, 29, 12, 77, 32, 87, 68, 94],
    [79,  3, 11, 99, 56, 70, 99, 60,  5, 56,  3, 61, 73, 75, 47, 14, 21, 86,  5, 77],
    [16, 89, 49, 15, 89, 45, 60, 23, 57, 64,  7,  1, 63, 41, 63, 47, 26, 75, 77, 40],
    [66, 58, 31, 68, 78, 91, 13, 59, 49, 85, 85,  9, 39, 41, 56, 40, 54, 77, 51, 31],
    [58, 56, 20, 85, 53, 35, 53, 41, 69, 13, 86, 72,  8, 49, 47, 87, 58, 18, 68, 28]
]
agents_count = 15

logger = logging.getLogger(__name__)

logger.debug("EMAS, %s agents", agents_count)
agents = unnamed_agents(agents_count, AggregateAgent)

stop_condition = lambda: TimeLimitStopCondition(10)

aggregated_agents = lambda: flow_shop_agents_initializer(20, len(time_matrix[0]), agents_count)

emas = EmasService

minimal_energy = lambda: 0
reproduction_minimum = lambda: 90
migration_minimum = lambda: 120
newborn_energy = lambda: 100
transferred_energy = lambda: 40


evaluation = lambda: FlowShopEvaluation(time_matrix)
crossover = lambda: PermutationCrossover()
mutation = lambda: PermutationMutation(1)
initializer = lambda: PermutationInitializer(len(time_matrix[0]))

address_provider = address.SequenceAddressProvider

migration = ParentMigration
locator = GridLocator


class FlowShopStatistics(WithGenomeStatistics):
    def __init__(self, file_name):
        self.output = open(file_name, 'w')
        self.time = time.time()
        self.best = None
        self.lastBest = None

    def update(self, step, agents):
        t = time.time() - self.time
        self.lastBest = self.best

        self.best = agents[0].get_best_genotype()
        for agent in agents:
            if agent.get_best_genotype().fitness > self.best.fitness:
                self.best = agent.get_best_genotype()

        if self.lastBest is None or self.lastBest.fitness < self.best.fitness:
            self.output.write('fitness: {2},\tgenome: {3} step: {0},time: {1:.3}\n'
                          .format(step, t, self.best.fitness, self.best.permutation))

    def summarize(self, agents):
        self.output.write('\n\n===================================================\n\n')
        self.output.write('Problem:\n')
        self.print_matrix(time_matrix)
        self.output.write('____________________________________________________\n\n')
        self.output.write('Best known solution: {0}\n'.format(self.best.permutation))
        makespan, result = evaluation().compute_makespan(self.best.permutation, True)

        self.output.write('Makespan: {0}\n'.format(int(makespan)))
        self.output.write('Time table:\n')
        self.print_matrix(result)
        self.output.flush()
        self.output.close()

    def print_matrix(self, matrix):
        for row in matrix:
            for i in row:
                val = str(int(i))
                self.output.write(val + (6 - len(val)) * ' ')
            self.output.write('\n')

stats = lambda: FlowShopStatistics('out_%s_pyage.txt' % __name__)
