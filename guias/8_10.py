# 8_10.py

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# H(z) = (z) / (z - 0.5)  => H(z) = 1 / (1 - 0.5z^-1)
zeros = [0]
poles = [0.5]
k = 1

# zeros = [0, 1]
# poles = [0.5, 1.5]
# k = 1

system_zpk = signal.dlti(zeros, poles, k, dt=1.0)

n_points = 100
n_1, y_1 = signal.dimpulse(system_zpk, n=n_points)
n_2, y_2 = signal.dstep(system_zpk, n=n_points)

# la salida de dimpulse es una lista, tomamos el primer elemento
h_n = y_1[0].flatten()
y_n = y_2[0].flatten()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# respuesta al impulso
markerline, stemlines, baseline = ax1.stem(n_1, h_n, basefmt=" ")
plt.setp(baseline, color='black', linewidth=0)
ax1.set_title('Respuesta al Impulso $h[n]$')
ax1.set_ylabel('Amplitud')
ax1.grid(True, linestyle='--', alpha=0.7)

# respuesta al escalon
markerline, stemlines, baseline = ax2.stem(n_2, y_n, basefmt=" ")
plt.setp(baseline, color='black', linewidth=0)
ax2.set_title('Respuesta al Escalón $y[n]$')
ax2.set_xlabel('Muestra ($n$)')
ax2.set_ylabel('Amplitud')
ax2.grid(True, linestyle='--', alpha=0.7)

plt.setp(baseline, color='black', linewidth=1)
plt.tight_layout()
plt.show()

# transferencia como diagrama de bode (modulo/fase)
w, h = signal.dfreqresp(system_zpk)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# magnitud
ax1.plot(w, 20 * np.log10(abs(h)))
ax1.set_title('Respuesta en Frecuencia (Magnitud)')
ax1.set_ylabel('Amplitud [dB]')
ax1.grid(True)

# fase
ax2.plot(w, np.angle(h))
ax2.set_title('Respuesta en Frecuencia (Fase)')
ax2.set_ylabel('Fase [rad]')
ax2.set_xlabel('Frecuencia [rad/muestra]')
ax2.grid(True)

plt.tight_layout()
plt.show()
