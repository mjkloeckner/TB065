# 7_17.py

import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, signal

T = 1/100 # seg
sample_rate = 1/T
sample_time = 1
N = int(sample_rate*sample_time)

for f1 in [30, 30.5]:
    for Nf in [N, 10*N]:
        for alpha in [0.5, 1, 5]:
            f2 = f1 + alpha/(N*T)

            # la frecuencia de muestreo de la señal es fija
            t = np.linspace(0, sample_time, int(N))
            y = np.cos(2*np.pi*f1*t) + np.cos(2*np.pi*f2*t)

            print(f1, f2)

            # calculo de DFT de Nf puntos
            Xf = np.fft.fft(t, n=Nf)
            freqs = np.fft.fftfreq(Nf, d=T)

            # centrar la frecuencia 0
            Xf = np.fft.fftshift(Xf)
            freqs = np.fft.fftshift(freqs)

            # grafico
            plt.figure(figsize=(8, 4))
            markerline, stemlines, baseline = plt.stem(freqs, np.abs(Xf))
            plt.setp(baseline, color='black', linewidth=0)
            plt.title(f"DFT con Nf={Nf}, f1={f1}, f2={f2:.2f}")
            plt.grid(True, linestyle=':', alpha=0.7)
            plt.grid(True, which='minor')
            plt.show()
