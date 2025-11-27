from utils import *
from scipy.signal import firwin, freqz, tf2zpk, get_window

############################# Tercera parte ###################################

cutoff = 2650    # frecuencia de corte
M = 700          # orden FIR (número de coeficientes)

def filtro_fir():
    # Diseño FIR pasabajos con ventana
    b = firwin(M, cutoff, fs=fs, window='hamming')

    w, H = freqz(b, worN=2048, fs=fs)
    fase = np.unwrap(np.angle(H))*180/np.pi

    fig, ax1, ax2 = freq_response_plot(w, H, fase, show=False)
    save_plot(fig, "respuesta_en_frecuencia_pasa-bajos_fir")

# `a` son los coeficientes de la respuesta al impulso (coinciden con los
# coeficientes de respuesta en frecuencia)
def filtro_fir_polos_y_ceros(a):
    zeros, poles, gain = tf2zpk(a, [1])

    # Crear figura
    fig, axis = plt.subplots(figsize=(8, 4))

    axis.scatter(np.real(zeros), np.imag(zeros),
                 s=25, facecolors='none', edgecolors='tab:blue', zorder=10,
                 label='Ceros', linewidth=1.25)

    axis.scatter(np.real(poles), np.imag(poles),
                 s=25, marker='x', color='tab:red',
                 label='Polos')

    axis.set_xlabel("Real", color="black")
    axis.set_ylabel("Imaginario", color="black")

    # Unidad círculo para referencia
    # theta = np.linspace(0, 2*np.pi, 100)
    # plt.plot(np.cos(theta), np.sin(theta))  # círculo unitario

    # axis.yaxis.set_major_locator(MaxNLocator(nbins=5))

    axis.grid(True, which='major', color='black', linestyle=':', linewidth=1.00)
    axis.grid(True, which='minor', color='black', linestyle=':', linewidth=0.50)
    axis.xaxis.set_minor_locator(AutoMinorLocator(2))

    plt.grid(True)
    plt.axis('equal')
    axis.legend()
    save_plot(fig, "polos_y_ceros_pasa-bajos_fir")


fs = 44100

# a diferencia de la funcion `filtro_fir` se genera el filtro mediante
# operaciones elementales, como la multiplicacion por ventana, en lugar de usar
# una funcion de libreria externa como `firwin`
def filtro_fir_deducido():
    # respuesta ideal pasabajos: sinc centrada en M/2
    n = np.arange(M + 1)
    wc = 2*np.pi*cutoff / fs

    # h_ideal = sinc(wc*n)/(pi n); wc = 2pi*fc/fs
    # se normaliza la ganancia a 1 multiplicando por 2.0*(fc/fs)
    h_ideal = np.sinc(2.0 * (cutoff/fs) * (n - M/2))

    # ventana de Hamming
    v_hamming = 0.54 - 0.46 * np.cos(2*np.pi*n/M)

    v_rectangular = [1 if i < 350 else 0 for i in range(0, M)]

    # respuesta del filtro FIR (version acotada de la sinc)
    h = h_ideal * v_hamming

    # se normaliza para tener ganancia unitaria para frecuancias <= fc
    h = h / np.sum(h)
    return h

def filtro_fir_analisis(h, fs):
    fig, ax = dtime_plot(M, h, "respuesta_al_impulso_filtro_fir",
                         f'Respuesta al impulso filtro FIR grado {M}')

    # respuesta en frecuencia del filtro
    w, H = freqz(h, worN=2048, fs=fs)
    fase = np.unwrap(np.angle(H)) * 180 / np.pi

    fig, ax1, ax2 = freq_response_plot(w, H, fase, show=False, fc=5e3)
    save_plot(fig, "respuesta_en_frecuencia_pasa-bajos_fir")

    # polos y ceros
    filtro_fir_polos_y_ceros(h)



"""
def ejemplo_cancion_filtrado_con_filtro_fir():
    # spectogram_plot(file_fs, file_data,
    #                 f"espectograma_fs_original_44100Hz", N=1024, ylim=[0, 20000])

    file_filter_output = np.convolve(file_data, h, mode='same')

    # spectogram_plot(file_fs, file_filter_output,
    #                 f"espectograma_fs_{cutoff}Hz", t=0, N=1024, ylim=[0, 20000])

    freq_plot(44100, v_hamming, "v_hamming_freq", f_max=8000)
    freq_plot(44100, v_rectangular, "v_rectangular_freq", f_max=8000)

    freq_compute_fft(44100, v_hamming)

    for i in [512, 1024, 2048]:
        # for window in ['boxcar', 'bartlett', 'hamming']:

        #     spectogram_plot(file1_fs, file_filter_output,
        #                     f"espectograma_submuestreado_{window}_{i:04d}", N=i,
        #                     win=window, ylim=[0, 3000], t=5, dt=1)

        N = 1024
        beta = 8.6
        kaiser_window = get_window(("kaiser", beta), N)
        spectogram_plot(file1_fs, file_filter_output,
                        f"espectograma_submuestreado_kaiser_window_{i:04d}", N=i,
                        win=kaiser_window, ylim=[0, 3000], t=5, dt=1)
"""
