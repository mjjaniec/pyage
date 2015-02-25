class PointGenotype(object):
    def __init__(self, x, y):
        super(PointGenotype, self).__init__()
        self.x = x
        self.y = y
        self.fitness = None

    def __str__(self):
        return "(%s, %s), f:%s" % (self.x, self.y, self.fitness)

    def __repr__(self):
        return self.__str__()


class FloatGenotype(object):
    def __init__(self, genes):
        super(FloatGenotype, self).__init__()
        self.fitness = None
        self.genes = genes

    def __str__(self):
        return "%s, f:%s" % (self.genes, self.fitness)

    def __repr__(self):
        return self.__str__()


class PermutationGenotype(object):
    def __init__(self, permutation):
        """
        :param permutation: order of processing
                a list of consecutive job numbers (0..n-1 NOT 1..n)
                NOT a list of orders of particular jobs

                e.g. a permutation (2,0,1) means that job2 is 1st, job0 2nd and job1 3rd
                NOT job0 is 3rd, job1 1st and job2 2nd
        :type permutation: list of int
        """
        self.permutation = permutation
        self.fitness = None

    def __str__(self):
        string = "PG[{0}, fitness: {1}]".format(self.permutation, self.fitness)
        return string if self.valid() else "INVALID!: " + string

    def __repr__(self):
        return self.__str__()

    def valid(self):
        """:rtype: bool"""
        r = [0] * len(self.permutation)
        for x in self.permutation:
            r[x] += 1
        return all(map(lambda q: q == 1, r))



