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


print("Reading words.")
CountWords = read_csv("CountWords_1")

print("Cleaning words.")
CleanCountWords = clean_words(CountWords)

sumWords = np.array([row[0] for row in CleanCountWords if row])
total_words = np.sum(sumWords)

frequencies = np.array([row / total_words for row in sumWords if row])
ranks = np.arange(1., float(len(frequencies)) + 1)

plt.plot(ranks, frequencies, 'b.', label='real data')

k, alpha = zipf_fit(frequencies, 0.01, 0.7)
plt.plot(ranks, zipf(ranks, k, alpha), 'y-', label=f'k={round(k,4)}, alpha={round(alpha,4)}')

popt, pcov = curve_fit(zipf, ranks, frequencies)
plt.plot(ranks, zipf(ranks, *popt), 'r-', label=f'fit k={round(popt[0],4)}, beta={round(popt[1],4)}')
print(f'Fit of k and alpha: {popt}')

plt.title('ZIPF')
plt.xlabel('Range')
plt.ylabel('Frequency')

plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.grid()

plt.show()
