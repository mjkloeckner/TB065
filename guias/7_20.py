# 7_20.py

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

fs = 400
T = 1/fs
t = np.arange(0, 1, T)

x_a = np.cos(2*np.pi*100*t)
x_b = (1 + np.cos(2*np.pi*10*t)) * np.cos(2*np.pi*100*t)
x_c = np.cos(2 * np.pi * 100 * t**2)

sig = [x_a, x_b, x_c]

plt.figure(figsize=(15, 5))

for i, x in enumerate(sig):
    plt.subplot(1, 3, i+1)

    # `nperseg` tamaño de la ventana
    # `noverlap` solapamiento entre ventanas
    f, times, Sxx = signal.spectrogram(x, fs, window='hann',
                                       nperseg=128, noverlap=32)

    plt.pcolormesh(times, f, 10*np.log10(Sxx), cmap='inferno', shading='gouraud')

    if i == 0:
        plt.ylabel('Frecuencia [Hz]')
    plt.xlabel('Tiempo [s]')

plt.tight_layout()
plt.show()
