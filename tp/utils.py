import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FuncFormatter

import matplotlib
import numpy as np
import os

plot_dir_name = 'plot'

matplotlib.rcParams['font.family'] = 'Inter'
matplotlib.rcParams['font.size'] = 12
matplotlib.use("TkAgg")

def ticks_label_format(x, pos):
    # 3 decimals, strip trailing zeros
    return f"{x:.3f}".rstrip("0").rstrip(".")

def graph_data(x, y, t=0, dt=0, a=0, da=0, y_min=0, y_max=0, show=True):
    figure, axis = plt.subplots(figsize=(5, 4))

    axis.plot(x, y, label='Señal de Audio')
    axis.set(xlabel='Tiempo [s]', ylabel='Amplitud normalizada')

    axis.minorticks_on()
    axis.grid(True, which='major', linestyle='-', linewidth=0.50)
    axis.grid(True, which='minor', linestyle=':', linewidth=0.50)

    # configuracion de ticks del eje x
    axis.xaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.xaxis.set_minor_locator(AutoMinorLocator(4))  # 2 subdivisions between majors

    plt.tight_layout()

    # max 3 decimals
    axis.xaxis.set_major_formatter(FuncFormatter(ticks_label_format))

    axis.set_xlim([t, t+dt if dt > 0 else x[-1]])
    axis.set_ylim(-1.1, 1.1)

    # resaltado de parte de la señal (solo si a != 0)
    axis.axvspan(a, a+da, color='skyblue',
                 alpha=0 if a == 0 else 0.50,
                 label=f"Un periodo T={da}s" if da != 0 else "")
    axis.legend()

    if show:
        plt.show()

    return figure, axis

def plot(fs, data, file_path="", t_start=0, t_width=0, a=0, da=0):
    # normaliza la amplitud dividiendo por el valor maximo del tipo de dato
    data = data.astype(np.float32)
    data /= np.max(np.abs(data))

    t = np.arange(len(data)) / fs
    fig, ax = graph_data(t, data, t=t_start, dt=t_width, a=a, da=da, show=False)

    if file_path != "":
        save_plot(fig, file_path, t_start=t_start, t_width=t_width)

    return fig, ax

def save_plot(fig, src_file_path, t_start=0, t_width=0, extra_name=''):
    basename = os.path.basename(src_file_path)
    file_name, ext = os.path.splitext(basename)
    fig_file_name = f'{plot_dir_name}/{file_name}'

    if t_start != 0:
        fig_name_append_1 = f'_{t_start}s'
        fig_name_append_2 = f'_a_{round(t_start + t_width, 3)}s' if t_width != 0 else ''
        fig_file_name += fig_name_append_1.replace('.', '_')
        fig_file_name += fig_name_append_2.replace('.', '_')

    fig_file_name += extra_name

    print(f'- "{fig_file_name}.png"')

     # crea carpeta para plots
    os.makedirs(plot_dir_name, exist_ok=True)
    fig.savefig(fig_file_name, dpi=300, bbox_inches="tight")
