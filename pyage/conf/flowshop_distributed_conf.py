# coding=utf-8
import logging
import os
import Pyro4

from pyage.core import address

from pyage.core.agent.agent import unnamed_agents
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import GridLocator, RandomLocator
from pyage.core.migration import ParentMigration, Pyro4Migration
from pyage.core.stats.statistics import FlowShopStatistics
from pyage.core.stop_condition import TimeLimitStopCondition
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
agents_count = 50

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
mutation = lambda: PermutationMutation(2)
initializer = lambda: PermutationInitializer(len(time_matrix[0]))

address_provider = address.SequenceAddressProvider

ns_hostname = lambda: os.environ['NS_HOSTNAME']
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon
migration = Pyro4Migration
locator = RandomLocator

stats = lambda: FlowShopStatistics('out_%s_pyage.txt' % __name__, time_matrix, evaluation())
