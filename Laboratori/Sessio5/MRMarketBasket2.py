"""
MRMarketBasket2
"""
from mrjob.job import MRJob
from mrjob.step import MRStep
# from itertools import groupby


class MRMarketBasket2(MRJob):

    def configure_args(self):
        """
        Additional configuration flag to get the groceries files
    
        :return:
        """
        super(MRMarketBasket2, self).configure_args()

    def mapper(self, _, line):
        """
        This is the mapper, it should generate one item count
        :param line: contains a transaction
        """
        # Each line is a string a,b,c
        trans = line.strip().split(',')
        # for key, group in groupby(trans):
        #     yield key, len(list(group))
        for t in trans:
            yield t, 1

    def reducer(self, key, values):
        """
        Input is an item as key and all the countings it has assigned
        Output should be at least a pair (key, new counting)
        """
        yield key, sum(values)

    def steps(self):
        return [MRStep(mapper=self.mapper, reducer=self.reducer)]


if __name__ == '__main__':
    MRMarketBasket2.run()
