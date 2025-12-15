# 2_19.py

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# `a` coeficientes de la entrada
# `b` coeficientes de las salida
def respuesta_impulso(a, b, N):
    a = np.array(a)
    b = np.array(b)

    # delta para la entrada
    x = np.zeros(N)
    x[0] = 1

    y = np.zeros(N)

    for n in range(N):
        # entrada
        parte_x = 0
        for i in range(len(a)):
            # condicion de reposo inicial
            if n - i >= 0:
                parte_x += a[i] * x[n - i]

        # salida
        parte_y = 0
        for j in range(1, len(b)):
            # condicion de reposo inicial
            if n - j >= 0:
                parte_y += b[j] * y[n - j]

        # normalizado por a0 (por si es distinto de 1)
        y[n] = (parte_x - parte_y) / a[0]

    return y

# `y(n) - 0.25*y(n - 1) = x(n)` coeficientes: a = [1, -0.5] y b = [1]
a = [1]
b = [1, -0.25]
N = 5

h = respuesta_impulso(a, b, N)
print(h) # [1.         0.25       0.0625     0.015625   0.00390625]
