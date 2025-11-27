import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FuncFormatter
from cycler import cycler

import matplotlib
import numpy as np
import os

from scipy.io import wavfile
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import spectrogram

plot_dir_name = 'plot'
out_dir_name = 'out'

matplotlib.rcParams['font.family'] = 'Inter'
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['axes.prop_cycle'] = cycler(
        color=['#1f77b4', '#ff0000', '#ff5f1f', 'green'])
matplotlib.use("TkAgg")

def ticks_label_format(x, pos):
    # 3 decimales, se eliminan los ceros y puntos
    return f"{x:.3f}".rstrip("0").rstrip(".")

def time_graph_multiple_data(x, y_arr, y_lab, t=0, dt=0, a=0, da=0, show=True):
    figure, axis = plt.subplots(figsize=(8, 4))

    for i, y in enumerate(y_arr):
        axis.plot(x, y, label=y_lab[i], alpha=0.75)

    axis.set(xlabel='Tiempo [s]', ylabel='Amplitud normalizada')

    axis.minorticks_on()
    axis.grid(True, which='major', color='black', linestyle=':', linewidth=1.00)
    axis.grid(True, which='minor', color='black', linestyle=':', linewidth=0.50)

    # configuracion de ticks del eje x
    axis.xaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.xaxis.set_minor_locator(AutoMinorLocator(5))

    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.yaxis.set_minor_locator(AutoMinorLocator(4))

    plt.tight_layout()

    # max 3 decimales
    axis.xaxis.set_major_formatter(FuncFormatter(ticks_label_format))

    axis.set_xlim([t, t+dt if dt > 0 else x[-1]])
    axis.set_ylim(-1.1, 1.1)

    # resaltado de parte de la señal (solo si a != 0)
    axis.axvspan(a, a+da, color='skyblue',
                 alpha=0 if a == 0 else 0.50,
                 label=f"Un periodo T={da}s" if da != 0 else "")
    axis.legend(loc='upper left')

    if show:
        plt.show()

    return figure, axis

# todos deben la misma cantidad de elementos que el primero
def time_plot_multiple(fs, data_arr, leg_arr, save_name="", t=0, dt=0, a=0, da=0, show=False):
    x = np.arange(len(data_arr[0])) / fs
    fig, ax = time_graph_multiple_data(x, data_arr, leg_arr, t, dt, a=a, da=da, show=show)

    if show == False:
        save_plot(fig, save_name)

    return fig, ax

def time_graph_data(x, y, t=0, dt=0, a=0, da=0, show=True):
    figure, axis = plt.subplots(figsize=(8, 4))

    axis.plot(x, y, label='Señal de audio')
    axis.set(xlabel='Tiempo [s]', ylabel='Amplitud normalizada')

    axis.minorticks_on()
    axis.grid(True, which='major', color='black', linestyle=':', linewidth=1.00)
    axis.grid(True, which='minor', color='black', linestyle=':', linewidth=0.50)

    # configuracion de ticks del eje x
    axis.xaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.xaxis.set_minor_locator(AutoMinorLocator(5))

    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.yaxis.set_minor_locator(AutoMinorLocator(4))

    plt.tight_layout()

    # max 3 decimales
    axis.xaxis.set_major_formatter(FuncFormatter(ticks_label_format))

    axis.set_xlim(t, t+dt if dt > 0 else x[-1])
    axis.set_ylim(-1.1, 1.1)

    # resaltado de parte de la señal (solo si a != 0)
    axis.axvspan(a, a+da, color='skyblue',
                 alpha=0 if a == 0 else 0.50,
                 label=f"Un periodo T={da}s" if da != 0 else "")
    axis.legend(loc='upper left')

    if show:
        plt.show()

    return figure, axis

def normalize(data):
    data = data.astype(np.float32)
    data /= np.max(np.abs(data))
    return data

def time_plot(fs, data, save_name="", t=0, dt=0, a=0, da=0):
    show = True if save_name == "" else False

    # normaliza la amplitud dividiendo por el valor maximo del tipo de dato
    data = normalize(data)

    x = np.arange(len(data)) / fs
    fig, ax = time_graph_data(x, data, t, dt, a, da, show)

    if show == False:
        save_plot(fig, save_name)

    return fig, ax

def save_plot(fig, name):
    base_name = os.path.basename(name)
    file_name, ext = os.path.splitext(base_name)
    file_path_no_ext = f'{plot_dir_name}/{file_name}'

    save_name = f'{file_path_no_ext}.png'
    print(save_name)

     # crea carpeta para plots
    os.makedirs(plot_dir_name, exist_ok=True)
    fig.savefig(save_name, dpi=250, bbox_inches="tight")
    plt.close(fig) # liberar memoria

def save_to_wav(fs, data, save_name):
    # normalizar para prevenir clipping
    data = data / np.max(np.abs(data))

    # convertir a 16-bit PCM para WAV
    data_as_int16 = np.int16(data * 32767)

    # crea carpeta para wavs
    os.makedirs(out_dir_name, exist_ok=True)

    file_path = f'{out_dir_name}/{save_name}'
    print(file_path)
    wavfile.write(file_path, fs, data_as_int16)

# frecuencia

# data = [[fft], [freqs], [legends]]
def freq_graph_multiple_data(data, f_min=0, f_max=0, y_min=0, y_max=0, show=True):
    fig, axis = plt.subplots(figsize=(8, 4))

    for i, (fft, freqs, label) in enumerate(data):
        # print(label)
        N = len(freqs)
        x = freqs[:N // 2]
        y = np.abs(fft[:N // 2])
        axis.plot(x, y, label=label, alpha=0.90, linewidth=((len(data)-i-1)*0.5 + 1.5))

    axis.set(xlabel='Frecuencia [Hz]', ylabel='Magnitud')

    axis.minorticks_on()
    axis.grid(True, which='major', color='black', linestyle=':', linewidth=1.00)
    axis.grid(True, which='minor', color='black', linestyle=':', linewidth=0.50)

    # configuracion de ticks del eje x
    axis.xaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.xaxis.set_minor_locator(AutoMinorLocator(5))

    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.yaxis.set_minor_locator(AutoMinorLocator(4))

    plt.tight_layout()

    # max 3 decimales
    axis.xaxis.set_major_formatter(FuncFormatter(ticks_label_format))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    axis.set_xlim([f_min, f_max if f_max != 0 else 20000])
    axis.set_ylim([y_min, y_max if y_max != 0 else 1.05*max(y)])

    axis.legend(loc='upper right')

    if show:
        plt.show()

    return fig, axis


def freq_graph_data(x, y, f_min=0, f_max=0, y_min=0, y_max=0, show=True):
    fig, axis = plt.subplots(figsize=(8, 4))

    axis.plot(x, y)
    axis.set(xlabel='Frecuencia [Hz]', ylabel='Magnitud')

    axis.minorticks_on()
    axis.grid(True, which='major', color='black', linestyle=':', linewidth=1.00)
    axis.grid(True, which='minor', color='black', linestyle=':', linewidth=0.50)

    # configuracion de ticks del eje x
    axis.xaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.xaxis.set_minor_locator(AutoMinorLocator(5))

    axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    axis.yaxis.set_minor_locator(AutoMinorLocator(4))

    plt.tight_layout()

    # max 3 decimales
    axis.xaxis.set_major_formatter(FuncFormatter(ticks_label_format))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    axis.set_xlim([f_min, f_max if f_max != 0 else 20000])
    axis.set_ylim([y_min, y_max if y_max != 0 else 1.05*max(y)])

    if show:
        plt.show()

    return fig, axis

def freq_compute_fft(fs, data, t=0, dt=0):
    i = 0
    di = fs*len(data)
    if t != 0 or dt != 0:
        i = int(t*fs)
        di = int((t+dt)*fs)

    interval_data = data[i:di]

    # puntos de la fft
    N = len(interval_data)
    interval_fft = fft(interval_data, 20000)
    interval_freqs = fftfreq(20000, d=1/fs)

    return interval_fft, interval_freqs

# hace la transformacion a frecuencias y pasa lo transformado a `freq_graph_data`
def freq_plot(fs, data, save_name="", f_min=0, f_max=0, y_min=0, y_max=0,
              t=0, dt=0, a=0, da=0, show=False):

    interval_fft, interval_freqs = freq_compute_fft(fs, data, t, dt)
    N = len(interval_fft)

    # se toma la parte positiva en ambos casos (primer parte del arreglo)
    x = interval_freqs[:N // 2]
    y = np.abs(interval_fft[:N // 2])

    fig, ax = freq_graph_data(x, y, f_min, f_max, y_min, y_max, show=show)

    if save_name != "":
        save_plot(fig, save_name)

    return fig, ax

# frecuencia de muestreo comun
# computa y grafica en una figura la fft the los datos en `data_arr`
def freq_plot_multiple(fs, data_arr, leg_arr, save_name="",
                       f_min=0, f_max=0, y_min=0, y_max=0, t=0, dt=0, show=True):

    fft_freqs_arr = []
    for i, data in enumerate(data_arr):
        fft, freqs = freq_compute_fft(fs, data, t, dt)
        fft_freqs_arr.append([fft, freqs, leg_arr[i]])

    fig, axis = freq_graph_multiple_data(fft_freqs_arr, f_min, f_max, y_min, y_max, show)

    if save_name != "":
        save_plot(fig, save_name)

def spectogram_plot(fs, data, save_name="", t=0, dt=0, N=1024, overlp=16, win='hamm', xlim=[], ylim=[], show=False):
    if dt == 0:
        dt = (len(data)/fs)-t

    i = int(t*fs)
    di = int((t+dt)*fs)
    interval_data = data[i:di]

    # `nperseg`  tamaño de ventana (número de muestras por segmento)
    # `noverlap` cantidad de solapamiento entre ventanas
    f, time, Sxx = spectrogram(interval_data, fs=fs, nperseg=N, noverlap=overlp,
                               window=win)
    fig, axis = plt.subplots(figsize=(8, 4))

    # plt.pcolormesh(time, f, Sxx**0.10, shading='gouraud')
    plt.pcolormesh(time, f, 10*np.log10(Sxx + 1e-12), shading='gouraud')

    plt.ylabel('Frecuencia [Hz]')
    plt.xlabel('Tiempo [s]')

    if len(xlim) != 0:
        plt.xlim(xlim)

    if len(ylim) != 0:
        plt.ylim(ylim)
    else:
        plt.ylim(1, 20000)

    if show == True:
        plt.show()
    else:
        if save_name != "":
            save_plot(fig, save_name)

    return fig, axis

def bode_plot(w, H, show=True):
    figure, axis = plt.subplots(figsize=(8, 4))

    axis.plot(w, 20*np.log10(np.abs(H)))

    axis.set(xlabel='Frecuencia [Hz]', ylabel='Magnitud [dB]')
    axis.minorticks_on()
    axis.grid(True, which='major', color='black', linestyle=':', linewidth=1.00)
    axis.grid(True, which='minor', color='black', linestyle=':', linewidth=0.50)
    plt.tight_layout()

    axis.set_xlim(0.0, 20e3)

    axis.legend(loc='upper left')

    if show:
        plt.show()

    return figure, axis

def freq_response_plot(w, H, phase, show=True, fc=20e3):
    fig, ax1 = plt.subplots(figsize=(8, 4))

    H_db = 20*np.log10(np.abs(H))

    line1, = ax1.plot(w, H_db)
    ax1.set(xlabel='Frecuencia [Hz]', ylabel='Magnitud [dB]')
    ax1.minorticks_on()
    ax1.grid(True, which='major', color='black', linestyle=':', linewidth=1.00)
    ax1.grid(True, which='minor', color='black', linestyle=':', linewidth=0.50)
    ax1.set_xlim(0.0, fc)

    ax2 = ax1.twinx()
    line2, = ax2.plot(w, phase, color="tab:red")
    ax2.set_ylabel("Fase [grados]", color="black")
    ax2.tick_params(axis='y', labelcolor="black")

    # axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))

    # Add ONE point

    # Find index closest to -3 dB
    idx = np.argmin(np.abs(H_db + 3))    # H_db = -3 => H_db +3 = 0
    w_3db = w[idx]
    H_3db = H_db[idx]
    line3 = ax1.scatter(w_3db, H_3db, color='tab:green', s=50, zorder=10)

    # nyquist
    w_nyquist = 2756.25
    idx = np.argmin(np.abs(w - w_nyquist))    # H_db = -3 => H_db +3 = 0
    H_nyquist = H_db[idx]
    line4 = ax1.scatter(w_nyquist, H_nyquist, color='tab:orange', s=50, zorder=10)

    ax1.legend([line1, line2, line3, line4],
               ["Magnitud [dB]",
                "Fase [grados]",
                r'-3dB $\approx$ %0.0f Hz'%w_3db,
                r'Nyquist $\approx$ %0.0f Hz'%w_nyquist],
               loc='upper right')

    plt.tight_layout()

    if show:
        plt.show()

    return fig, ax1, ax2

def dtime_plot(N, f, save_name="", legend="", n=0, dn=0, a=0, da=0):
    show = True if save_name == "" else False

    n = np.arange(N + 1)

    fig, axis = plt.subplots(figsize=(8,4))
    axis.set(xlabel='Tiempo discreto', ylabel='Amplitud')

    markerline, stemlines, baseline = axis.stem(
        n, f,
        markerfmt='o',     # tipo de marcador en la cabeza
        basefmt="k-",
    )

    markerline.set_markersize(2.0)
    stemlines.set_linewidth(0.35)
    baseline.set_linewidth(0.5)

    stemlines.set_zorder(2)
    markerline.set_zorder(3)
    baseline.set_zorder(1)

    axis.grid(True, which='major', color='black', linestyle=':', linewidth=1.00)
    axis.grid(True, which='minor', color='black', linestyle=':', linewidth=0.50)
    axis.set_xlim(0, N+1)
    axis.set_ylim(-0.03, 0.15)

    # configuracion de ticks del eje x
    axis.xaxis.set_major_locator(MaxNLocator(nbins=15))
    axis.xaxis.set_minor_locator(AutoMinorLocator(2))

    axis.yaxis.set_minor_locator(AutoMinorLocator(2))

    # axis.yaxis.set_major_locator(MaxNLocator(nbins=5))
    # axis.yaxis.set_minor_locator(AutoMinorLocator(4))

    if legend != "":
        axis.legend([markerline], [legend], loc='upper right')

    if show == False:
        save_plot(fig, save_name)
    else:
        plt.show()

    return fig, axis

# np.linspace(start, stop, num).astype(int)
