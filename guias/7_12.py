# 7_12.py

import numpy as np
import matplotlib.pyplot as plt

w = np.linspace(-np.pi, np.pi, 1000)
h = 1 - np.exp(-1j * 5 * w)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# magnitud
ax1.plot(w, np.abs(h))
ax1.set_title(r'Magnitud $|1 - e^{-j5\omega}|$')
ax1.set_ylabel('Amplitud')
ax1.set_xticks([-np.pi, -2*np.pi/5, 0, 2*np.pi/5, np.pi])
ax1.set_xticklabels([r'$-\pi$', r'$-2\pi/5$', '0', r'$2\pi/5$', r'$\pi$'])
ax1.grid(True)

# fase
ax2.plot(w, np.angle(h))
ax2.set_title(r'Fase $\angle H(e^{j\omega})$')
ax2.set_ylabel('Fase [rad]')
ax2.set_xlabel('Frecuencia [rad/muestra]')
ax2.grid(True)

plt.tight_layout()
plt.show()
