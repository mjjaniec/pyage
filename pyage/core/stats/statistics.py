import logging
import os
import urllib2
import time
import sys
from pyage.core.inject import InjectOptional, Inject

logger = logging.getLogger(__name__)


class Statistics(object):
    def update(self, step_count, agents):
        raise NotImplementedError()

    def summarize(self, agents):
        raise NotImplementedError()


class WithGenomeStatistics(Statistics):
    def __init__(self, file_name):
        self.output = open(file_name, 'w')
        self.time = time.time()

    def update(self, step, agents):
        t = time.time() - self.time
        self.best = agents[0].get_best_genotype()

        for agent in agents:
            if agent.get_best_genotype().fitness > self.best.fitness:
                self.best = agent.get_best_genotype()

        self.output.write('fitness: {2},\tgenome: {3} step: {0},time: {1:.3}\n'
                          .format(step, t, self.best.fitness, self.best.permutation))

    def summarize(self, agents):
        self.output.flush()
        self.output.close()


class SimpleStatistics(Statistics):
    def __init__(self, plot_file_name='plot.png'):
        self.history = []
        self.plot_file_name = plot_file_name

    def update(self, step_count, agents):
        try:
            best_fitness = max(a.get_fitness() for a in agents)
            logger.info(best_fitness)
            self.history.append(best_fitness)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            import pylab
            logger.debug(self.history)
            logger.debug("best genotype: %s", max(agents, key=lambda a: a.get_fitness).get_best_genotype())
            pylab.yscale('symlog')
            pylab.savefig(self.plot_file_name)
        except:
            logging.exception("")


class TimeStatistics(SimpleStatistics):
    @InjectOptional("notification_url")
    def __init__(self, plot_file_name='plot.png'):
        super(TimeStatistics, self).__init__(plot_file_name)
        self.times = []
        self.start = time.time()

    def update(self, step_count, agents):
        super(TimeStatistics, self).update(step_count, agents)
        try:
            self.times.append(time.time() - self.start)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            import pylab
            pylab.plot(self.times, self.history)
            pylab.xlabel("time (s)")
            pylab.ylabel("fitness")
            pylab.yscale('symlog')
            pylab.savefig(self.plot_file_name)

            if hasattr(self, "notification_url"):
                url = self.notification_url + "?time=%s&agents=%s&conf=%s" % (
                    time.time() - self.start, os.environ['AGENTS'], sys.argv[1])
                logger.info(url)
                urllib2.urlopen(url)
            logger.debug(self.history)
            logger.debug("best genotype: %s", max(agents, key=lambda a: a.get_fitness).get_best_genotype())
        except:
            logging.exception("")


class NotificationStatistics(SimpleStatistics):
    @Inject("notification_url")
    def __init__(self):
        super(NotificationStatistics, self).__init__()
        self.start = time.time()

    def summarize(self, agents):
        try:
            url = self.notification_url + "?time=%s&agents=%s&conf=%s" % (
                time.time() - self.start, os.environ['AGENTS'], sys.argv[1])
            logger.info(url)
            urllib2.urlopen(url)

        except:
            logging.exception("")


class NoStatistics(Statistics):
    def update(self, step_count, agents):
        pass

    def summarize(self, agents):
        pass


class FlowShopStatistics(WithGenomeStatistics):
    def __init__(self, file_name, time_matrix, evaluation):
        self.output = open(file_name, 'w')
        self.time = time.time()
        self.time_matrix = time_matrix
        self.best = None
        self.lastBest = None
        self.evaluation = evaluation

    def update(self, step, agents):
        t = time.time() - self.time
        self.lastBest = self.best

        self.best = agents[0].get_best_genotype()
        for agent in agents:
            if agent.get_best_genotype().fitness > self.best.fitness:
                self.best = agent.get_best_genotype()

        if self.lastBest is None or self.lastBest.fitness < self.best.fitness:
            print -self.best.fitness
            self.output.write('fitness: {2},\tgenome: {3} step: {0},time: {1:.3}\n'
                          .format(step, t, self.best.fitness, self.best.permutation))

    def summarize(self, agents):
        self.output.write('\n\n===================================================\n\n')
        self.output.write('Problem:\n')
        self.print_matrix(self.time_matrix)
        self.output.write('____________________________________________________\n\n')
        self.output.write('Best known solution: {0}\n'.format(self.best.permutation))
        makespan, result = self.evaluation.compute_makespan(self.best.permutation, True)

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
