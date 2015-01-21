import logging

import launcher_config_small as l_conf
from pyage.core import inject
from pyage.core.address import SequenceAddressProvider
from pyage.core.agent.agent import unnamed_agents, generate_agents, Agent
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import RandomLocator
from pyage.core.migration import NoMigration, ParentMigration
from pyage.core.stats.statistics import FlowShopStatistics
from pyage.core.stop_condition import TimeLimitStopCondition
from pyage.core.workplace import Workplace
from pyage.launcher.constants import emas, classic, matrix
from pyage.solutions.evolution.crossover.permutation import FirstHalfSwapsCrossover
from pyage.solutions.evolution.evaluation import FlowShopEvaluation
from pyage.solutions.evolution.initializer import flow_shop_agents_initializer, PermutationInitializer
from pyage.solutions.evolution.mutation import PermutationMutation, MemeticPermutationMutation
from pyage.solutions.evolution.selection import TournamentSelection


__author__ = 'mjjaniec'

logger = logging.getLogger(__name__)


def main():
    for config in l_conf.configs:
        for number_of_aggregates in l_conf.numbers_of_aggregates:
            for aggregate_size in l_conf.aggregate_sizes:
                for stages in l_conf.memetic_stages:
                    for obj in l_conf.matrices:
                        msg = "type: {0}, agents: {1}, pop: {2}, mem: {3}".format(config, number_of_aggregates,
                                                                                  aggregate_size, stages)
                        print msg
                        logger.info(msg)
                        lunch_computation(config, number_of_aggregates, aggregate_size, stages, obj)


def create_base_params():
    return {
        "stop_condition": lambda: TimeLimitStopCondition(10),
        "locator": RandomLocator,
        "logger": lambda: logger,
        "address_provider": lambda: SequenceAddressProvider(),
        "stats": lambda: FlowShopStatistics('out_%s_pyage.txt' % __name__)
    }


def create_resolver(params):
    def resolver(conf, conf_arg_name, args):
        try:
            return params[args[0].address.split('.')[0] + '__' + conf_arg_name]()
        except:
            return params[conf_arg_name]()

    return resolver


def create_emas_params(agents_count, agent_population, time_matrix, stages):
    return {
        "agents": unnamed_agents(agents_count, AggregateAgent),
        "aggregated_agents": lambda: flow_shop_agents_initializer(agent_population, len(time_matrix[0]), agents_count),
        "emas": EmasService,

        "minimal_energy": lambda: 0,
        "reproduction_minimum": lambda: 90,
        "migration_minimum": lambda: 120,
        "newborn_energy": lambda: 100,
        "transferred_energy": lambda: 40,

        "initializer": lambda: PermutationInitializer(len(time_matrix[0])),
        "evaluation": lambda: FlowShopEvaluation(time_matrix),
        "crossover": lambda: FirstHalfSwapsCrossover(),
        "mutation": lambda: PermutationMutation(2) if stages == 0 else MemeticPermutationMutation(stages, 8, 2),

        "migration": ParentMigration
    }


def create_classic_params(agents_count, agent_population, time_matrix, stages):
    return {
        "agents": generate_agents("flowshop", agents_count, Agent),
        "initializer": lambda: PermutationInitializer(len(time_matrix[0]), agent_population),
        "evaluation": lambda: FlowShopEvaluation(time_matrix),
        "operators": lambda: [
            FirstHalfSwapsCrossover(),
            PermutationMutation(2) if stages == 0 else MemeticPermutationMutation(stages, 8, 2),
            FlowShopEvaluation(time_matrix),
            TournamentSelection(agent_population, agent_population)
        ],
        "migration": NoMigration
    }


def lunch_computation(config, agents_count, agent_population, stages, obj):
    base_params = create_base_params()
    specific_params = {}
    if config == emas:
        specific_params = create_emas_params(agents_count, agent_population, obj[matrix], stages)
    elif config == classic:
        specific_params = create_classic_params(agents_count, agent_population, obj[matrix], stages)

    inject.resolve_attr = create_resolver(dict(base_params.items() + specific_params.items()))
    inject.Inject.read_config = lambda self, string: None

    workplace = Workplace()
    workplace.publish()
    while not workplace.stopped:
        workplace.step()
    workplace.unregister()


if __name__ == "__main__":
    main()