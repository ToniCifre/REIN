import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import re

from commons import *


def zipf(x, k, a):
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
wordsList = read_csv("CountWords")

print("Cleaning words.")
cleanWordsList = clean_words(wordsList)
# frequencies = np.array([int(row[0]) for row in wordsList if row])
total_words = np.sum(cleanWordsList)

frequencies = np.array([row / total_words for row in cleanWordsList if row])
ranks = np.arange(1., float(len(frequencies)) + 1)

plt.plot(ranks, frequencies, 'b.', label='real data')
plt.plot(ranks, zipf(ranks, 1, 1), 'y-', label='k=1, a=1')

popt, pcov = curve_fit(zipf, ranks, frequencies)
print(f'Fit of k and alpha: {popt}')
plt.plot(ranks, zipf(ranks, *popt), 'r-', label=f'fit {popt}')


plt.title('ZIPF')
plt.xlabel('Range')
plt.ylabel('Frequency')

plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.grid()

plt.show()
