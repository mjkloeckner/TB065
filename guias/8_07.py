# 8_07.py

import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin

tau = 0.1

T = 2 * pi  # Periodo
w0 = 2 * pi / T
D = 0.5 # duty cycle

k_max = 100
ks = np.arange(k_max, dtype=int)
a_k = np.arange(k_max, dtype=float)
b_k = np.arange(k_max, dtype=float)

for k in range(k_max):
    if k == 0:
        a_k[k] = (w0*D*T) / (2*pi)
        b_k[k] = (1/((tau*2*pi/T)+1)) * (w0*D*T)/(2*pi)
    else:
        a_k[k] = sin(k*D*w0*T/2) / (k*pi)
        b_k[k] = (1/((tau*2*pi/T)+1)) * (sin(k*D*w0*T/2)/(k*pi))

# magnitud a_k
plt.subplot(1, 2, 1)
markerline, stemlines, _ = plt.stem(ks, np.abs(a_k), basefmt=" ")
plt.setp(markerline, 'markerfacecolor', 'blue')
plt.title('Espectro de Magnitud $|a_k|$')
plt.xlabel('Armónico (k)')
plt.ylabel('Amplitud')
plt.grid(True, linestyle='--')

# fase a_k
plt.subplot(1, 2, 2)
plt.stem(ks, np.angle(a_k), basefmt=" ")
plt.title('Espectro de Fase $\\angle a_k$ (rad)')
plt.xlabel('Armónico (k)')
plt.ylabel('Fase')
plt.grid(True, linestyle='--')

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 10))

# magnitud b_k
plt.subplot(1, 2, 1)
markerline, stemlines, _ = plt.stem(ks, np.abs(b_k), basefmt=" ")
plt.setp(markerline, 'markerfacecolor', 'blue')
plt.title('Espectro de Magnitud $|b_k|$')
plt.xlabel('Armónico (k)')
plt.ylabel('Amplitud')
plt.grid(True, linestyle='--')

# fase b_k
plt.subplot(1, 2, 2)
plt.stem(ks, np.angle(b_k), basefmt=" ")
plt.title('Espectro de Fase $\\angle b_k$ (rad)')
plt.xlabel('Armónico (k)')
plt.ylabel('Fase')
plt.grid(True, linestyle='--')

plt.tight_layout()
plt.show()
