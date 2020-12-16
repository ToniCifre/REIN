"""
MRMarketBasket1
"""
import itertools

from mrjob.job import MRJob
from mrjob.step import MRStep


class MRMarketBasket1(MRJob):

    def configure_args(self):
        """
        Additional configuration flag to get the groceries files
    
        :return:
        """
        super(MRMarketBasket1, self).configure_args()

    def mapper(self, _, line):
        """
        This is the mapper, it should generate pairs of items
        :param line: contains a transaction
        """
        trans = list(line.strip().split(','))
        trans.sort(reverse=True)
        for i in range(len(trans) - 1):
            for t in range(i + 1, len(trans)):
                yield f'{trans[i]}#{trans[t]}', 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        """
        Input is a pair of items as key and all the countings it has assigned
        Output should be at least a pair (key, new counting)
        """
        yield key, sum(values)

    def steps(self):
        return [MRStep(mapper=self.mapper, combiner=self.combiner, reducer=self.reducer)]


if __name__ == '__main__':
    MRMarketBasket1.run()