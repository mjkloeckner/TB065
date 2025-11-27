from utils import *

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


