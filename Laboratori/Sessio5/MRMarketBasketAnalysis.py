"""
.. module:: MRMarketBasketAnalysis

MRMarketBasketAnalysis
*************

:Description: MRMarketBasketAnalysis

    Executes the MRMarketBasket1 and MRMarketBasket2 scripts


:Created on: 17/07/2020

"""

from MRMarketBasket1 import MRMarketBasket1
from MRMarketBasket2 import MRMarketBasket2
import argparse
import time
from mrjob.util import to_lines
import pandas as pd
import subprocess

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='groceries.csv', help='Groceries file')
    parser.add_argument('--ncores', default=4, type=int, help='Number of parallel processes to use')
    args = parser.parse_args()
   
    tinit = time.time()  # For timing the execution

    mr_job1 = MRMarketBasket1(args=['-r', 'local', args.file, '--num-cores', str(args.ncores)])
    with mr_job1.make_runner() as runner1:
        runner1.run()
        pairs = pd.DataFrame(mr_job1.parse_output(runner1.cat_output()))
        pairs.columns = ['key', 'suma']
        print(pairs.head())

    mr_job2 = MRMarketBasket2(args=['-r', 'local', args.file,'--num-cores', str(args.ncores)])
    with mr_job2.make_runner() as runner2:
        runner2.run()
        singles = dict(mr_job2.parse_output(runner2.cat_output()))

    print(f'Time= {(time.time() - tinit)} seconds')

    # Get the total number of transaction in the file given as argument
    ntrans = int(subprocess.check_output(["wc", "-l", args.file]).decode("utf8").split()[0])
    print(f'\nNumber of transactions {ntrans}\n')

    pairs[['key1', 'key2']] = pairs.key.str.split("#", n=1, expand=True)

    # pairs["support"] = pairs.apply(lambda row: row['suma'] / ntrans, axis=1)
    # pairs['conf1'] = pairs.apply(lambda row: row['suma'] / singles[row['key1']], axis=1)
    # pairs['conf2'] = pairs.apply(lambda row: row['suma'] / singles[row['key2']], axis=1)

    pairs["support"] = pairs.suma / ntrans
    pairs['conf1'] = pairs.suma / pairs.key1.map(singles)
    pairs['conf2'] = pairs.suma / (pairs.key2.map(singles))

    print(pairs.sort_values(['suma'], ascending=[False]).head(20))
    print(pairs.shape)

    print("******************************************************************************* ")
    print("************ Values and rules to fill the required table ********************** ")
    print("******************************************************************************* ")
    # nr = 'toni'
    for support, conf in [(0.01,0.01),(0.01,0.25),(0.01,0.5),(0.01,0.75),(0.05,0.25),(0.07,0.25),(0.20,0.25),(0.5,0.25)]:

        toni = pairs[pairs.support > support]
        # toni.reset_index(drop=True, inplace=True)
        nr = toni[toni.conf1 > conf].size
        nr += toni[toni.conf2 > conf].size
 
        print("Support=", str(support),"confidence=", str(conf)+".", "Rules found", nr, '\n')
    

