import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import zetac
import pylab
import re

from commons import *


def Zipf(x, k, a):
    return k * (x ** -a)


def clean_words(words):
    aux = []
    pattern = re.compile("[A-Za-z][a-z]{2}")
    for row in words:
        if pattern.match(row[1]) and int(row[0]) >= 4:
            print(row[0])
            aux.append(int(row[0]))

    print(f'{len(words) - len(aux)} words removed.')
    return aux


print("Reading words.")
CountWords = read_csv("CountWords")
print("Cleaning words.")
# frequencies = clean_words(CountWords)
frequencies = np.array([int(row[0]) for row in CountWords if row])
total_words = np.sum(frequencies)

frequencies = np.array([row / total_words for row in frequencies if row])
ranks = np.arange(1., float(len(frequencies)) + 1)

plt.plot(ranks, frequencies, 'b.', label='real data')
plt.plot(ranks, Zipf(ranks, 1, 1), 'y-', label='k=1, a=1')

popt, pcov = curve_fit(Zipf, ranks, frequencies)
print(*popt)
plt.plot(ranks, Zipf(ranks, *popt), 'r-', label=f'fit {popt}')

# popt, pcov = curve_fit(Zipf, ranks, frequencies, bounds=(0.01, [2., 2.]))
# print(*popt)
# print(*pcov)
# plt.plot(ranks, Zipf(ranks, *popt), 'g--', label='fit-with-bounds')

plt.xscale('log')
plt.yscale('log')

plt.title('ZIPF')

plt.xlabel('Range')
plt.ylabel('Frequency')

plt.legend()
plt.grid()

plt.show()
