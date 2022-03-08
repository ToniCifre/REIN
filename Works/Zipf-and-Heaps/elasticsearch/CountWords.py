"""
.. module:: CountWords

CountWords
*************

:Description: CountWords

    Generates a list with the counts and the words in the 'text' field of the documents in an index

:Version: 

:Date:  5/06/2020

"""

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError, TransportError

from commons import *

import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--alpha', action='store_true', default=False, help='Sort words alphabetically')
    args = parser.parse_args()

    index = args.index

    try:
        client = Elasticsearch()
        voc = {}
        sc = scan(client, index=index, query={"query": {"match_all": {}}})
        for s in sc:
            try:
                tv = client.termvectors(index=index, id=s['_id'], fields=['text'])
                if 'text' in tv['term_vectors']:
                    for t in tv['term_vectors']['text']['terms']:
                        if t in voc:
                            voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                        else:
                            voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
            except TransportError:
                pass

        lpal = []
        for v in voc:
            lpal.append((v.encode("utf-8", "ignore"), voc[v]))

        csv_rowlist = []
        total_words = 0
        for pal, cnt in sorted(lpal, key=lambda x: x[0 if args.alpha else 1], reverse=True):
            csv_rowlist.append([cnt, pal.decode("utf-8")])
            total_words += cnt

        print('--------------------')
        print(f'Different {len(lpal)} Words')
        print(f'{total_words} Total Words')

        write_csv(csv_rowlist, "CountWords")

    except NotFoundError:
        print(f'Index {index} does not exists')
