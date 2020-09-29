import numpy as np
import matplotlib.pyplot as plt

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError, TransportError

from scipy.optimize import curve_fit


def heaps(n, k, beta):
    return k * (n ** beta)


index = 'inovels'  # inovels_1, inovels_2

aux = [0]
try:
    voc = {}
    client = Elasticsearch()
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

except NotFoundError:
    print(f'Index {index} does not exists')
    exit(1)

ranks = np.arange(1., len(aux) + 1)
ranks2 = np.arange(1., 260000)

popt, pcov = curve_fit(heaps, ranks, aux)

plt.plot(ranks, aux, 'b-', label=f'Real Data')
plt.plot(ranks2, heaps(ranks2, *popt), 'y-', label=f'fit k={round(popt[0], 2)}, beta={round(popt[1], 2)}')

plt.plot(ranks2, ranks2, 'r-')

plt.title('HEAPS')
plt.legend()
plt.grid()

plt.show()
