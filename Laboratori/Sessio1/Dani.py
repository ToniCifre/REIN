from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError, TransportError

import argparse, math
import matplotlib.pyplot as plt
import numpy as np
# from sklearn.linear_model import LinearRegression


def Zipf(frequency, r_times, dwnTrim, topTrim):
    # Calcular la recta de regresion para obtener m y b
    # A partir de alli recalcular los valores de frequencia
    # Devolveremos la array con las nuevas frecuencias y la linea de regresión

    logF = []
    rF = []
    dwnTrim = int(len(freq) * dwnTrim)
    topTrim = int((len(freq) - 1) * topTrim)
    for f in frequency:
        if f > frequency[topTrim] and f < frequency[dwnTrim]:
            logF.append(math.log10(f))

    for i in range(len(logF)):
        rF.append(math.log10(i + 1))

    m, b = np.polyfit(rF, logF, 1)
    alpha = -m
    k = 10 ** b

    nFreq = []
    for r in r_times:
        nFreq.append(k * (r ** (-alpha)))

    return nFreq


def Heaps(f, N):
    # Falta per crear la funcio de Heaps, com hem fet la de Zipf
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default='inovels', required=False, help='Index to search')
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

        zipf = True
        r = []
        freq = []
        i = 1
        for palabra, cnt in sorted(lpal, key=lambda x: x[0 if not zipf else 1], reverse=True):
            freq.append(cnt)
            r.append(i)
            i = i + 1

        # nFreq = Zipf(freq, r, 0.01, 0.7)

        plt.title('Zipf\'s Law')
        plt.plot(r, freq, 'bo')
        plt.plot(r, Zipf(freq, r, 0, 1), 'r', label="0/1")
        plt.plot(r, Zipf(freq, r, 0.01, 0.8), 'y', label="0.01/0.8")
        plt.plot(r, Zipf(freq, r, 0.01, 0.6), 'g', label="0.01/0.6")
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.show()


    except NotFoundError:
        print(f'Index {index} does not exists')