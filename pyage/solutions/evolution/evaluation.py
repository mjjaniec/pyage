from math import cos, pi, sin, sqrt

from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import PointGenotype, FloatGenotype, PermutationGenotype


A = 10


class FloatRastriginEvaluation(Operator):
    def __init__(self):
        super(FloatRastriginEvaluation, self).__init__(FloatGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__rastrigin(genotype.genes)

    def __rastrigin(self, genes):
        sum = len(genes) * A
        for gene in genes:
            sum += gene ** 2 - A * cos(2 * pi * gene)
        return sum


class RastriginEvaluation(Operator):
    def __init__(self):
        super(RastriginEvaluation, self).__init__(PointGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__rastrigin(genotype.x, genotype.y)

    def __rastrigin(self, x, y):
        return 2 * A + x ** 2 - A * cos(2 * pi * x) + y ** 2 - A * cos(2 * pi * y)


class DeJongEvaluation(Operator):
    def __init__(self, type=None):
        super(DeJongEvaluation, self).__init__(PointGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__DeJong(genotype.x, genotype.y)

    def __DeJong(self, x, y):
        return x ** 2 + y ** 2


class SchwefelEvaluation(Operator):
    def __init__(self):
        super(SchwefelEvaluation, self).__init__()

    def process(self, population):
        for genotype in population:
            genotype.fitness = - self.__schwefel(genotype.genes)

    def __schwefel(self, genes):
        sum = 418.9829
        for gene in genes:
            sum += -gene * sin(sqrt(abs(gene)))
        return sum


class FlowShopEvaluation(Operator):
    def __init__(self, time_matrix):
        super(FlowShopEvaluation, self).__init__(PermutationGenotype)
        self.time_matrix = time_matrix
        self.JOBS_COUNT = len(self.time_matrix[0]) + 1  # + 1: for sentinel column
        self.PROCESSORS_COUNT = len(self.time_matrix) + 1  # + 1: for sentinel row

    def process(self, population):
        """ :type population: list of PermutationGenotype """
        for individual in population:
            individual.fitness = - self.compute_makespan(individual.permutation)

    def compute_makespan(self, permutation, compute_solution_matrix=False):
        """ :return: makespan for processing in order specified by :param permutation: """
        completion_times = self._calculate_completion_times(permutation)
        if compute_solution_matrix:
            return completion_times[-1][-1], completion_times
        else:
            return completion_times[-1][-1]

    def _calculate_completion_times(self, permutation):
        completion_times = self._initialize_including_sentinels()
        for pi in xrange(1, self.PROCESSORS_COUNT):
            for ji in xrange(1, self.JOBS_COUNT):
                completion_times[pi][ji] = self.time_matrix[pi - 1][permutation[ji - 1]] \
                                           + max(completion_times[pi][ji - 1], completion_times[pi - 1][ji])
        completion_times = self._strip_sentinels(completion_times)
        return completion_times

    def _initialize_including_sentinels(self):
        return [[0 for job_i in xrange(self.JOBS_COUNT)]
                for processor_i in xrange(self.PROCESSORS_COUNT)]

    @staticmethod
    def _strip_sentinels(completion_times):
        return [processor[1:] for processor in completion_times[1:]]


class OpenShopEvaluation(Operator):
    def __init__(self, time_matrix):
        super(OpenShopEvaluation, self).__init__(PermutationGenotype)
        self.time_matrix = time_matrix
        self.JOBS_COUNT = len(self.time_matrix[0])
        self.PROCESSORS_COUNT = len(self.time_matrix)

    def process(self, population):
        """ :type population: list of PermutationGenotype """
        for individual in population:
            individual.fitness = - self.compute_makespan(individual.permutation)

    def compute_makespan(self, permutation):
        jobs_cts = self._calculate_jobs_completion_times(permutation)
        return max(jobs_cts)

    def _calculate_jobs_completion_times(self, permutation):
        def update_cts(ct):
            processors_cts[proc_id] = ct
            jobs_cts[job_id] = ct

        # cts - completion_times
        processors_cts = [0 for _ in range(self.PROCESSORS_COUNT)]
        jobs_cts = [0 for _ in range(self.JOBS_COUNT)]
        for permutation_item in permutation:
            job_id, proc_id = self._decode_ids(permutation_item)
            can_start_at = max(processors_cts[proc_id], jobs_cts[job_id])
            task_time = self.time_matrix[proc_id][job_id]
            update_cts(can_start_at + task_time)
        return jobs_cts

    def _decode_ids(self, permutation_item):
        proc_id = permutation_item % self.PROCESSORS_COUNT
        job_id = permutation_item // self.PROCESSORS_COUNT
        return job_id, proc_id
