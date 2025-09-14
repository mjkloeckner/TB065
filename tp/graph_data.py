import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator
import matplotlib
import numpy as np

matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.use("TkAgg")

def graph_data(x, y, t=0, dt=0, a=0, da=0, y_min=0, y_max=0, show=True):
    figure, axis = plt.subplots(figsize=(10, 8))

    axis.plot(x, y, label='Señal de Audio')
    axis.set(xlabel='Tiempo [s]', ylabel='Amplitud normalizada')

    axis.minorticks_on()
    axis.grid(True, which='major', linestyle='-')
    axis.grid(True, which='minor', linestyle=':', linewidth=0.5)

    # configuracion de ticks del eje x
    axis.xaxis.set_major_locator(MaxNLocator(nbins=18))  # ~18 ticks por plot
    axis.xaxis.set_minor_locator(MaxNLocator(nbins=72))

    axis.set_xlim([t, t+dt if dt > 0 else x[-1]])
    axis.set_ylim([y_min if y_min != 0 else axis.get_ylim()[0],
                   y_max if y_max != 0 else axis.get_ylim()[1]])

    # resaltado de parte de la señal (solo si a != 0)
    axis.axvspan(a, a+da, color='skyblue',
                 alpha=0 if a == 0 else 0.50,
                 label=f"Un periodo T={da}s" if da != 0 else "")
    axis.legend()

    if show:
        plt.show()

    return figure, axis
