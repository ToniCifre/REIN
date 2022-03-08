import math
import numpy as np
import matplotlib.pyplot as plt

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError, TransportError

import numpy as np
import matplotlib.pyplot as plt

from commons import *
from scipy.optimize import curve_fit


def heaps(n, k, beta):
    return k * (n ** beta)


index = 'inovels_2'

try:
    client = Elasticsearch()
    voc = {}
    aux = [0]
    sc = scan(client, index=index, query={"query": {"match_all": {}}})
    for s in sc:
        try:
            tv = client.termvectors(index=index, id=s['_id'], fields=['text'])
            if 'text' in tv['term_vectors']:
                for t in tv['term_vectors']['text']['terms']:
                    if t in voc:
                        voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                        aux.append(aux[-1])
                    else:
                        voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
                        aux.append(aux[-1] + 1)
        except TransportError:
            pass

    ranks = np.arange(1., len(aux) + 1)
    ranks2 = np.arange(1., 260000)

    popt, pcov = curve_fit(heaps, ranks, aux)
    plt.plot(ranks2, heaps(ranks2, *popt), 'y-', label=f'fit k={round(popt[0],2)}, beta={round(popt[1],2)}')
    print(f'Fit of k and alpha: {popt}')

    plt.plot(ranks, aux, 'b-', label=f'Real Data')
    plt.plot(ranks2, ranks2, 'r-')

    plt.title('HEAPS')
    plt.legend()
    plt.grid()
    plt.grid()

    plt.show()

except NotFoundError:
    print(f'Index {index} does not exists')
