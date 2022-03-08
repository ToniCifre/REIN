import numpy as np
import matplotlib.pyplot as plt

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError, TransportError

from scipy.optimize import curve_fit


def heaps(n, k, beta):
    return k * (n ** beta)


index = 'news' # 'inovels'  # inovels_1, inovels_2

aux = [0]
nWords = 0
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
                        aux.append(nWords)
                    else:
                        voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
                        nWords += 1
                        aux.append(nWords)
        except TransportError:
            pass

except NotFoundError:
    print(f'Index {index} does not exists')
    exit(1)

ranks = np.arange(1., len(aux) + 1)

popt, pcov = curve_fit(heaps, ranks, aux)

plt.plot(ranks, aux, 'b-', label=f'Real Data')
plt.plot(ranks, heaps(ranks, *popt), 'y-', label=f'fit k={round(popt[0], 2)}, beta={round(popt[1], 2)}')

plt.plot(ranks, ranks, 'r-')

plt.title('HEAPS')
plt.legend()
plt.grid()

plt.show()
