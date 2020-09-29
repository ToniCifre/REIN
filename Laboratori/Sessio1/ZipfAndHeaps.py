
import re
import math
import numpy as np
import matplotlib.pyplot as plt

from commons import *
from scipy.optimize import curve_fit


def zipf(x, k, alpha):
    return k * (x ** (-alpha))


def zipf_fit(frequency, dwnTrim, topTrim):
    # Calcular la recta de regresion para obtener m y b
    # A partir de alli recalcular los valores de frequencia
    # Devolveremos la array con las nuevas frecuencias y la linea de regresión

    logF = []
    rF = []
    dwnTrim = int(len(frequency) * dwnTrim)
    topTrim = int((len(frequency) - 1) * topTrim)
    for f in frequency:
        if frequency[topTrim] < f < frequency[dwnTrim]:
            logF.append(math.log10(f))

    for i in range(len(logF)):
        rF.append(math.log10(i + 1))

    m = np.polyfit(rF, logF, 1)
    print(m)
    alpha = -m[0]
    k = 10 ** m[1]
    return k, alpha


def clean_words(words):
    aux = []
    pattern = re.compile("[A-Za-z][a-z'a-z]{2,9}")
    for row in words:
        if pattern.match(row[1]) and int(row[0]) >= 4:
            aux.append(int(row[0]))

    print(f'{len(words) - len(aux)} words removed.')
    return aux


print("Reading words.")
CountWords = read_csv("CountWords")
print("Cleaning words.")
frequencies = clean_words(CountWords)
# frequencies = np.array([int(row[0]) for row in CountWords if row])
total_words = np.sum(frequencies)

frequencies = np.array([row / total_words for row in frequencies if row])
ranks = np.arange(1., float(len(frequencies)) + 1)

plt.plot(ranks, frequencies, 'b.', label='real data')

k, alpha = zipf_fit(frequencies, 0.01, 0.7)
plt.plot(ranks, zipf(ranks, k, alpha), 'y-', label=f'k={k}, a={alpha}')
k, alpha = zipf_fit(frequencies, 0, 1)
plt.plot(ranks, zipf(ranks, k, alpha), 'g-', label=f'k={k}, a={alpha}')
k, alpha = zipf_fit(frequencies, 0.05, 0.6)
plt.plot(ranks, zipf(ranks, k, alpha), 'b-', label=f'k={k}, a={alpha}')


popt, pcov = curve_fit(zipf, ranks, frequencies)
print(f'Fit of k and alpha: {popt}')
plt.plot(ranks, zipf(ranks, *popt), 'r-', label=f'fit {popt}')


plt.xscale('log')
plt.yscale('log')

plt.title('ZIPF')

plt.xlabel('Range')
plt.ylabel('Frequency')

plt.legend()
plt.grid()

plt.show()
