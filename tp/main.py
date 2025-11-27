import numpy as np
from scipy.io import wavfile
from scipy.signal import firwin, freqz, tf2zpk, get_window
from utils import *
import librosa

## Datos
file1_path          = 'data/cancion1.wav'
file2_path          = 'data/cancion2.wav'
filter1_h_file_path = 'data/respuesta_impulso_1.txt'
filter2_h_file_path = 'data/respuesta_impulso_2.txt'

a4_flauta_file_path    = 'data/a4_flauta.wav'
a4_clarinete_file_path = 'data/a4_clarinete.wav'
a4_violin_file_path    = 'data/a4_violin.wav'

file1_fs, file1_data = wavfile.read(file1_path)
file2_fs, file2_data = wavfile.read(file2_path)
filter1_h = np.loadtxt(filter1_h_file_path)
filter2_h = np.loadtxt(filter2_h_file_path)

a4_flauta_fs, a4_flauta_data = wavfile.read(a4_flauta_file_path)
a4_clarinete_fs, a4_clarinete_data = wavfile.read(a4_clarinete_file_path)
a4_violin_fs, a4_violin_data = wavfile.read(a4_violin_file_path)

file1_filter1_output = np.convolve(file1_data, filter1_h, mode='same')
file1_filter2_output = np.convolve(file1_data, filter2_h, mode='same')
file2_filter1_output = np.convolve(file2_data, filter1_h, mode='same')
file2_filter2_output = np.convolve(file2_data, filter2_h, mode='same')

############################## Primera Parte ###################################

def time_domain_cancion1():
    ### grafico completo
    time_plot(file1_fs, file1_data, file1_path)

    ### porciones cuasi-periodicas 'cancion1'
    time_plot(file1_fs, file1_data, "cancion1_0_248s_a_0_256s",
               t=0.248, dt=0.008, a=0.24978, da=0.003)

    time_plot(file1_fs, file1_data, "cancion1_0_520s_a_0_528s",
               t=0.520, dt=0.008, a=0.5208, da=0.003)

    ### salida de filtro 'cancion1'
    save_to_wav(file1_fs, file1_filter1_output, "file1_filter1_output.wav")
    save_to_wav(file1_fs, file1_filter2_output, "file1_filter2_output.wav")

    ### grafico comparando la muestra 1 original y filtrada 1
    data_arr = [normalize(file1_data), normalize(file1_filter1_output)]
    leg_arr = ['Señal de audio', 'Señal de audio filtrada']

    time_plot_multiple(file1_fs, data_arr, leg_arr,
                       "cancion1_filter1_output_compare")

    time_plot_multiple(file1_fs, data_arr, leg_arr,
                       "cancion1_filter1_output_compare_0_248_a_0_256",
                       t=0.248, dt=0.008)

    ### grafico comparando la muestra 1 original y filtrada 2
    data_arr = [normalize(file1_data), normalize(file1_filter2_output)]
    leg_arr = ['Señal de audio', 'Señal de audio filtrada']

    time_plot_multiple(file1_fs, data_arr, leg_arr,
                       "cancion1_filter2_output_compare")
    time_plot_multiple(file1_fs, data_arr, leg_arr,
                       "cancion1_filter2_output_compare_0_248_a_0_256",
                       t=0.248, dt=0.008)

def time_domain_cancion2():
    ### grafico completo
    time_plot(file2_fs, file2_data, "cancion2", t=6)

    ### porciones cuasi-periodicas 'cancion2'
    time_plot(file2_fs, file2_data, "cancion2_14_72s_a_14_73s", t=14.720, dt=0.01)
    time_plot(file2_fs, file2_data, "cancion2_26_57s_a_26_58s", t=26.570, dt=0.01)

    save_to_wav(file2_fs, file2_filter1_output, "file2_filter1_output.wav")
    save_to_wav(file2_fs, file2_filter2_output, "file2_filter2_output.wav")

    ### grafico comparando la muestra 2 original y filtrada 2
    data_arr = [normalize(file2_data), normalize(file2_filter1_output)]
    leg_arr = ['Señal original', 'Señal filtrada']

    time_plot_multiple(file2_fs, data_arr, leg_arr,
                       "cancion2_6s_filter1_output_compare", t=6)
    time_plot_multiple(file2_fs, data_arr, leg_arr,
                       "cancion2_6s_filter1_output_compare_26_57_a_26_58",
                       t=26.57, dt=0.01)

    ### grafico comparando la muestra 2 original y filtrada 2
    data_arr = [normalize(file2_data), normalize(file2_filter2_output)]
    leg_arr = ['Señal original', 'Señal filtrada']

    time_plot_multiple(file2_fs, data_arr, leg_arr,
                       "cancion2_6s_filter2_output_compare", t=6)
    time_plot_multiple(file2_fs, data_arr, leg_arr,
                       "cancion2_6s_filter2_output_compare_26_57_a_26_58",
                       t=26.57, dt=0.01)

def time_domain_music_instruments():
    ### grafico de los instrumentos musicales
    time_plot(a4_flauta_fs, a4_flauta_data, "a4_flauta", t=0.25, dt=0.010)
    time_plot(a4_clarinete_fs, a4_clarinete_data, "a4_clarinete", t=0.25, dt=0.010)
    time_plot(a4_violin_fs, a4_violin_data, "a4_violin", t=0.25, dt=0.010)


############################## Segunda parte ##################################

def freq_domain_cancion1():
    freq_plot(file1_fs, file1_data, "cancion1_fft", f_max=8000)
    freq_plot(file1_fs, file1_filter1_output, "cancion1_filter1_output_fft",
              f_max=8000)
    freq_plot(file1_fs, file1_filter2_output, "cancion1_filter2_output_fft",
              f_max=8000)

def freq_domain_cancion2():
    freq_plot(file2_fs, file2_data, "cancion2_fft",
              f_max=8000)
    freq_plot(file2_fs, file2_filter1_output, "cancion2_filter1_output_fft",
              f_max=8000)
    freq_plot(file2_fs, file2_filter2_output, "cancion2_filter2_output_fft",
              f_max=8000)

def freq_domain_spectograms():
    # Formas de funcion ventana (en tiempo, en frecuencia tienen otra forma)
    # 'boxcar': rectangular
    # 'bartlett': triangular
    # 'hann': similar a medio ciclo de seno
    # https://en.wikipedia.org/wiki/Window_function

    for i in [512, 1024, 2048]:
        for window in ['boxcar', 'bartlett', 'hann', 'hamming']:
            spectogram_plot(file1_fs, file1_data,
                            f"cancion1_espectograma_{window}_{i:04d}", N=i,
                            win=window, ylim=[0, 17500])

            spectogram_plot(file2_fs, file2_data,
                            f"cancion2_espectograma_{window}_{i:04d}", t=6, N=i,
                            win=window, ylim=[0, 8000])

def a4_flauta_cutoff():
    a4_flauta_cutoff_fft, a4_flauta_cutoff_freqs = freq_compute_fft(
            a4_flauta_fs, a4_flauta_data)

    # armonicos mayores a 'cutoff_freq' Hz son descartadas, analogo a aplicar un
    # filtro pasabajos ideal

    cutoff_freq = 1000
    a4_flauta_cutoff_fft[np.abs(a4_flauta_cutoff_freqs) > cutoff_freq] = 0.0

    # espectro de la señal filtrada
    N = len(a4_flauta_cutoff_fft)
    x = a4_flauta_cutoff_freqs[:N // 2]
    y = np.abs(a4_flauta_cutoff_fft[:N // 2])
    fig, axis = freq_graph_data(x, y, f_max=2000, show=False)
    save_plot(fig, f"a4_flauta_cutoff_{cutoff_freq}Hz_fft")

    # señal temporal reconstruida
    a4_flauta_cutoff = ifft(a4_flauta_cutoff_fft).real

    time_plot(a4_flauta_fs, a4_flauta_cutoff,
              f"a4_flauta_cutoff_{cutoff_freq}Hz", 0.25, 0.010)

    save_to_wav(a4_flauta_fs, a4_flauta_cutoff,
                f"a4_flauta_cutoff_{cutoff_freq}Hz.wav")

    data_arr = [normalize(a4_flauta_data), normalize(a4_flauta_cutoff)]
    leg_arr = [
        'Señal de nota A4 de flauta',
        'Señal de nota A4 de flauta filtrada'
    ]
    time_plot_multiple(a4_flauta_fs, data_arr, leg_arr,
                       "a4_flauta_cutoff_time_comparison", t=0.25, dt=0.008)

    data_arr = [a4_flauta_cutoff, a4_flauta_data]
    leg_arr = ["Nota musical A4 con flauta filtrada", "Nota musical A4 con flauta"]
    freq_plot_multiple(a4_flauta_fs, data_arr, leg_arr, f_max=4000, t=0.253,
                       dt=8*0.002272727, save_name="a4_flauta_comparison", show=False)

def a4_clarinete_cutoff():
    a4_clarinete_cutoff_fft, a4_clarinete_cutoff_freqs = freq_compute_fft(
            a4_clarinete_fs, a4_clarinete_data)

    cutoff_freq = 3000
    a4_clarinete_cutoff_fft[np.abs(a4_clarinete_cutoff_freqs) > cutoff_freq] = 0.0

    # espectro de la señal filtrada
    N = len(a4_clarinete_cutoff_fft)
    x = a4_clarinete_cutoff_freqs[:N // 2]
    y = np.abs(a4_clarinete_cutoff_fft[:N // 2])
    fig, axis = freq_graph_data(x, y, f_max=3000, show=False)
    save_plot(fig, f"a4_clarinete_cutoff_{cutoff_freq}Hz_fft")

    # señal temporal reconstruida
    a4_clarinete_cutoff = ifft(a4_clarinete_cutoff_fft).real
    time_plot(a4_clarinete_fs, a4_clarinete_cutoff,
              f"a4_clarinete_cutoff_{cutoff_freq}Hz", 0.25, 0.010)
    save_to_wav(a4_clarinete_fs, a4_clarinete_cutoff,
                f"a4_clarinete_cutoff_{cutoff_freq}Hz.wav")

    data_arr = [normalize(a4_clarinete_data), normalize(a4_clarinete_cutoff)]
    leg_arr = [
        'Señal de nota A4 de clarinete',
        'Señal de nota A4 de clarinete filtrada'
    ]
    time_plot_multiple(a4_clarinete_fs, data_arr, leg_arr,
                       "a4_clarinete_cutoff_time_comparison", t=0.25, dt=0.008)

    data_arr = [a4_clarinete_cutoff, a4_clarinete_data]
    leg_arr = [
        "Nota musical A4 con clarinete filtrada",
        "Nota musical A4 con clarinete"
    ]

    freq_plot_multiple(a4_clarinete_fs, data_arr, leg_arr, f_max=8000, t=0.253,
                       dt=8*0.002272727, save_name="a4_clarinete_comparison", show=False)

def a4_violin_cutoff():
    a4_violin_cutoff_fft, a4_violin_cutoff_freqs = freq_compute_fft(
            a4_violin_fs, a4_violin_data)

    cutoff_freq = 4000
    a4_violin_cutoff_fft[np.abs(a4_violin_cutoff_freqs) > cutoff_freq] = 0.0

    # espectro
    N = len(a4_violin_cutoff_fft)
    x = a4_violin_cutoff_freqs[:N // 2]
    y = np.abs(a4_violin_cutoff_fft[:N // 2])
    fig, axis = freq_graph_data(x, y, f_max=4000, show=False)
    save_plot(fig, f"a4_violin_cutoff_{cutoff_freq}Hz_fft")

    # señal temporal reconstruida
    a4_violin_cutoff = ifft(a4_violin_cutoff_fft).real
    time_plot(a4_violin_fs, a4_violin_cutoff,
              f"a4_violin_cutoff_{cutoff_freq}Hz", 0.25, 0.010)
    save_to_wav(a4_violin_fs, a4_violin_cutoff, f"a4_violin_cutoff_{cutoff_freq}Hz.wav")

    data_arr = [normalize(a4_violin_data), normalize(a4_violin_cutoff)]
    leg_arr = ['Señal de nota A4 de violin', 'Señal de nota A4 de violin filtrada']
    time_plot_multiple(a4_violin_fs, data_arr, leg_arr,
                       "a4_violin_cutoff_time_comparison", t=0.25, dt=0.008)

    data_arr = [a4_violin_cutoff, a4_violin_data]
    leg_arr = ["Nota musical A4 con violin filtrada", "Nota musical A4 con violin"]
    freq_plot_multiple(a4_violin_fs, data_arr, leg_arr, f_max=8000, t=0.253,
                       dt=8*0.002272727, save_name="a4_violin_comparison", show=False)

def a4_flauta_fseries():
    fft_freqs_arr = []

    for i in [8, 4, 1]:
        fft, freqs = freq_compute_fft(a4_flauta_fs, a4_flauta_data, t=0.253, dt=i*0.002272727)
        fft_freqs_arr.append([fft, freqs,
              f"Serie de Fourier {i} periodo{'s' if i != 1 else ''}"])

    fig, axis = freq_graph_multiple_data(fft_freqs_arr, show=False, f_max=4500)
    save_plot(fig, "a4_flauta_fseries_comparison")

def a4_clarinete_fseries():
    fft_freqs_arr = []

    for i in [8, 4, 1]:
        fft, freqs = freq_compute_fft(
                a4_clarinete_fs, a4_clarinete_data, t=0.253, dt=i*0.002272727)

        fft_freqs_arr.append([fft, freqs,
              f"Serie de Fourier {i} periodo{'s' if i != 1 else ''}"])

    fig, axis = freq_graph_multiple_data(fft_freqs_arr, show=False, f_max=8000)
    save_plot(fig, "a4_clarinete_fseries_comparison")

def a4_violin_fseries():
    fft_freqs_arr = []

    for i in [8, 4, 1]:
        fft, freqs = freq_compute_fft(a4_violin_fs, a4_violin_data,
                                      t=0.253, dt=i*0.002272727)
        fft_freqs_arr.append([fft, freqs,
              f"Serie de Fourier {i} periodo{'s' if i != 1 else ''}"])

    fig, axis = freq_graph_multiple_data(fft_freqs_arr, show=False, f_max=8000)
    save_plot(fig, "a4_violin_fseries_comparison")


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


def filtro_fir_deducido():
    fs = 44100

    # respuesta ideal pasabajos: sinc centrada en M/2
    n = np.arange(M + 1)
    wc = 2*np.pi*cutoff / fs

    # h_ideal = sinc(wc*n)/(pi n); wc = 2pi*fc/fs
    # se normaliza la ganancia a 1 multiplicando por 2.0*(fc/fs)
    h_ideal = np.sinc(2.0 * (cutoff/fs) * (n - M/2))

    # ventana de Hamming
    v_hamming = 0.54 - 0.46 * np.cos(2*np.pi*n/M)

    v_rectangular = []
    for i in n:
        v_rectangular.append(1 if i < 350 else 0)

    # respuesta del filtro FIR (version acotada de la sinc)
    h = h_ideal * v_hamming

    # se normaliza para tener ganancia unitaria para frecuancias <= fc
    h = h / np.sum(h)

    # fig, ax = dtime_plot(M, h, "respuesta_al_impulso_filtro_fir",
    #                      f'Respuesta al impulso filtro FIR grado {M}')

    # respuesta en frecuencia del filtro
    w, H = freqz(h, worN=2048, fs=fs)
    fase = np.unwrap(np.angle(H)) * 180 / np.pi

    # fig, ax1, ax2 = freq_response_plot(w, H, fase, show=False, fc=5e3)
    # save_plot(fig, "respuesta_en_frecuencia_pasa-bajos_fir")

    # polos y ceros
    # filtro_fir_polos_y_ceros(h)

    file_path = 'canciones/000002.mp3'

    file_data, file_fs = librosa.load(file_path, sr=None, mono=True)
    file_fs = int(fs)

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

############################# Llamados a funciones ############################

def primer_y_segunda_parte():
    # time_domain
    time_domain_cancion1()
    time_domain_cancion2()
    time_domain_music_instruments()

    # freq_domain
    freq_domain_cancion1()
    freq_domain_cancion2()
    freq_domain_spectograms()

    freq_plot(48000, filter1_h, "filter1_h_fft", f_max=2000)
    freq_plot(48000, filter2_h, "filter2_h_fft", f_max=8000)

    a4_flauta_fseries()
    a4_clarinete_fseries()
    a4_violin_fseries()

    # obs: para realizar el filtrado se toma toda la señal no solo un periodo
    a4_flauta_cutoff()
    a4_clarinete_cutoff()
    a4_violin_cutoff()


# primer_y_segunda_parte()
filtro_fir_deducido()
