# coding=utf-8
import Pyro4

from pyage.core import address
from pyage.core.agent import  agents_factory, aggregate_agents_factory
from pyage.core.locator import  ParentLocator
from pyage.core.migration import Pyro4Migration
from pyage.core.statistics import SimpleStatistics
from pyage.solutions.evolution.crossover import AverageCrossover
from pyage.solutions.evolution.evaluation import RastriginEvaluation
from pyage.solutions.evolution.initializer import PointInitializer, emas_initializer
from pyage.solutions.evolution.mutation import UniformPointMutation
from pyage.solutions.evolution.selection import TournamentSelection

agents = aggregate_agents_factory("aggregate")

step_limit = lambda: 100

aggregated_agents = lambda: emas_initializer(energy=10, size=1000, lowerbound=-100, upperbound=100)

evaluation = RastriginEvaluation
crossover = AverageCrossover
mutation = lambda: UniformPointMutation(probability=1)

address_provider = address.AddressProvider

migration = Pyro4Migration
locator = ParentLocator

ns_hostname = lambda: "192.168.0.103"
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon

stats = SimpleStatistics