"""
MRMarketBasket1
"""
from mrjob.job import MRJob
from mrjob.step import MRStep
from itertools import groupby


class MRMarketBasket1(MRJob):

    def configure_args(self):
        """
        Additional configuration flag to get the groceries files
    
        :return:
        """
        super(MRMarketBasket1, self).configure_args()
        # self.add_file_arg('--file', )

    def mapper(self, _, line):
        """
        This is the mapper, it should generate pairs of items
        :param line: contains a transaction
        """
        trans = line.strip().split(',')

        for key, group in groupby(trans):
            yield key, len(list(group))

    def reducer(self, key, values):
        """
        Input is a pair of items as key and all the countings it has assigned
        Output should be at least a pair (key, new counting)
        """

        yield key, sum(values)

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]


if __name__ == '__main__':
    MRMarketBasket1.run()
