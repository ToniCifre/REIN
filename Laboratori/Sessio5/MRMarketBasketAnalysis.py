"""
.. module:: MRMarketBasketAnalysis

MRMarketBasketAnalysis
*************

:Description: MRMarketBasketAnalysis

    Executes the MRMarketBasket1 and MRMarketBasket2 scripts


:Created on: 17/07/2020

"""
import time
import argparse
import subprocess
import pandas as pd

from prettytable import PrettyTable

from MRMarketBasket1 import MRMarketBasket1
from MRMarketBasket2 import MRMarketBasket2

from mrjob.util import to_lines

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='groceries.csv', help='Groceries file')
    parser.add_argument('--ncores', default=4, type=int, help='Number of parallel processes to use')
    args = parser.parse_args()

    tinit = time.time()  # For timing the execution

    mr_job1 = MRMarketBasket1(args=['-r', 'local', args.file, '--num-cores', str(args.ncores)])
    print('Runing job 1 ...', end='')
    with mr_job1.make_runner() as runner1:
        runner1.run()
        pairs = pd.DataFrame(mr_job1.parse_output(runner1.cat_output()))
        pairs.columns = ['key', 'suma']
        # print(pairs.head())
    print(' [ok]')

    mr_job2 = MRMarketBasket2(args=['-r', 'local', args.file, '--num-cores', str(args.ncores)])
    print('Runing job 2 ...', end='')
    with mr_job2.make_runner() as runner2:
        runner2.run()
        singles = dict(mr_job2.parse_output(runner2.cat_output()))
    print(' [ok]')

    print(f'Time= {(time.time() - tinit)} seconds')

    # Get the total number of transaction in the file given as argument
    ntrans = int(subprocess.check_output(["wc", "-l", args.file]).decode("utf8").split()[0])
    print(f'\nNumber of transactions {ntrans}\n')

    pairs[['key1', 'key2']] = pairs.key.str.split("#", n=1, expand=True)

    pairs["support"] = pairs.suma / ntrans
    pairs['conf1'] = pairs.suma / pairs.key1.map(singles)
    pairs['conf2'] = pairs.suma / pairs.key2.map(singles)

    # print(pairs.sort_values(['suma'], ascending=[False]).head(20))

    print("******************************************************************************* ")
    print("************ Values and rules to fill the required table ********************** ")
    print("******************************************************************************* ")
    for support, conf in [(0.01, 0.01), (0.01, 0.25), (0.01, 0.5), (0.01, 0.75), (0.05, 0.25), (0.07, 0.25),
                          (0.20, 0.25), (0.5, 0.25)]:

        supp = pairs[pairs.support >= support]
        conf1 = supp[supp.conf1 >= conf]
        conf2 = supp[supp.conf2 >= conf]

        nr = conf1.shape[0] + conf2.shape[0]

        print("\nSupport=", str(support), "confidence=", str(conf) + ".", "Rules found", nr)

        if 0 < nr < 10:
            pt = PrettyTable(['Product 1', 'Product 2', 'Support', 'Confidence'])
            pt.sortby = "Support"
            pt.reversesort = True

            pt.align["Product 1"] = "l"
            pt.align["Product 2"] = "l"

            for index, row in conf1.iterrows():
                pt.add_row([row["key1"], row["key2"], row["support"], row["conf1"]])
                # print(f'- {row["key1"]} -> {row["key2"]} with s={row["support"]} and c={row["conf1"]}')
            for index, row in conf2.iterrows():
                pt.add_row([row["key2"], row["key1"], row["support"], row["conf2"]])
                # print(f'- {row["key2"]} -> {row["key1"]} with s={row["support"]} and c={row["conf2"]}')

            print(pt.get_string(title="Association Rules"))
