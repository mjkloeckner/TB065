import numpy as np
from scipy.io import wavfile
from utils import *

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

file1_filter1_output = np.convolve(file1_data, filter1_h, mode='same')
file1_filter2_output = np.convolve(file1_data, filter2_h, mode='same')

file2_filter1_output = np.convolve(file2_data, filter1_h, mode='same')
file2_filter2_output = np.convolve(file2_data, filter2_h, mode='same')

## 'cancion1'
def time_domain_cancion1():
    ### grafico completo
    time_plot(file1_fs, file1_data, file1_path)

    ### porciones cuasi-periodicas 'cancion1'
    time_plot(file1_fs, file1_data, "cancion1_0_248s_a_0_256s",
               t_start=0.248, t_width=0.008, a=0.24978, da=0.003)

    time_plot(file1_fs, file1_data, "cancion1_0_520s_a_0_528s",
               t_start=0.520, t_width=0.008, a=0.5208, da=0.003)

    ### salida de filtro 'cancion1'
    save_convolved_to_wav(file1_filter1_output, file1_fs, "file1_filter1_output.wav")
    save_convolved_to_wav(file1_filter2_output, file1_fs, "file1_filter2_output.wav")

    ### grafico comparando la muestra 1 original y filtrada 1
    data_arr = [normalize(file1_data), normalize(file1_filter1_output)]
    leg_arr = ['Señal de audio', 'Señal de audio filtrada']

    time_plot_multiple(file1_fs, data_arr, leg_arr, "cancion1_filter1_output_compare.png")
    time_plot_multiple(file1_fs, data_arr, leg_arr, "cancion1_filter1_output_compare_0_248_a_0_256", t=0.248, dt=0.008)

    ### grafico comparando la muestra 1 original y filtrada 2
    data_arr = [normalize(file1_data), normalize(file1_filter2_output)]
    leg_arr = ['Señal de audio', 'Señal de audio filtrada']

    time_plot_multiple(file1_fs, data_arr, leg_arr, "cancion1_filter2_output_compare")
    time_plot_multiple(file1_fs, data_arr, leg_arr,
                       "cancion1_filter2_output_compare_0_248_a_0_256", t=0.248, dt=0.008)

## 'cancion2'
def time_domain_cancion2():
    ### grafico completo
    time_plot(file2_fs, file2_data, "cancion2", t_start=6)

    ### porciones cuasi-periodicas 'cancion2'
    time_plot(file2_fs, file2_data, "cancion2_14_72s_a_14_73s", t_start=14.720, t_width=0.01)
    time_plot(file2_fs, file2_data, "cancion2_26_57s_a_26_58s", t_start=26.570, t_width=0.01)

    save_convolved_to_wav(file2_filter1_output, file2_fs, "file2_filter1_output.wav")
    save_convolved_to_wav(file2_filter2_output, file2_fs, "file2_filter2_output.wav")

    ### grafico comparando la muestra 2 original y filtrada 2
    data_arr = [normalize(file2_data), normalize(file2_filter1_output)]
    leg_arr = ['Señal original', 'Señal filtrada']

    time_plot_multiple(file2_fs, data_arr, leg_arr, "cancion2_6s_filter1_output_compare", t=6)
    time_plot_multiple(file2_fs, data_arr, leg_arr, "cancion2_6s_filter1_output_compare_26_57_a_26_58", t=26.57, dt=0.01)

    ### grafico comparando la muestra 2 original y filtrada 2
    data_arr = [normalize(file2_data), normalize(file2_filter2_output)]
    leg_arr = ['Señal original', 'Señal filtrada']

    time_plot_multiple(file2_fs, data_arr, leg_arr, "cancion2_6s_filter2_output_compare", t=6)
    time_plot_multiple(file2_fs, data_arr, leg_arr, "cancion2_6s_filter2_output_compare_26_57_a_26_58", t=26.57, dt=0.01)

def time_domain_music_instruments():
    ## Sonido de instrumentos musicales
    a4_flauta_fs, a4_flauta_data = wavfile.read(a4_flauta_file_path)
    a4_clarinete_fs, a4_clarinete_data = wavfile.read(a4_clarinete_file_path)
    a4_violin_fs, a4_violin_data = wavfile.read(a4_violin_file_path)

    ### grafico de los instrumentos musicales
    time_plot(a4_flauta_fs, a4_flauta_data, "a4_flauta", t_start=0.25, t_width=0.010)
    time_plot(a4_clarinete_fs, a4_clarinete_data, "a4_clarinete", t_start=0.25, t_width=0.010)
    time_plot(a4_violin_fs, a4_violin_data, "a4_violin", t_start=0.25, t_width=0.010)

def time_domain():
    time_domain_cancion1()
    time_domain_cancion2()
    time_domain_music_instruments()

def freq_domain_cancion1():
    freq_plot(file1_fs, file1_data, "cancion1_fft", f_max=8000, y_max=1e8)
    freq_plot(file1_fs, file1_filter1_output, "cancion1_filter1_output_fft",
              f_max=8000, y_max=1e8)
    freq_plot(file1_fs, file1_filter2_output, "cancion1_filter2_output_fft",
              f_max=8000, y_max=1e8)

def freq_domain_cancion2():
    freq_plot(file2_fs, file2_data, "cancion2_fft",
              f_max=8000, y_max=0.5e8)
    freq_plot(file2_fs, file2_filter1_output, "cancion2_filter1_output_fft",
              f_max=8000, y_max=0.5e8)
    freq_plot(file2_fs, file2_filter2_output, "cancion2_filter2_output_fft",
              f_max=8000, y_max=0.5e8)

def freq_domain():
    freq_domain_cancion1()
    freq_domain_cancion2()

    freq_plot(48000, filter1_h, "filter1_h_fft", f_max=2000)
    freq_plot(48000, filter2_h, "filter2_h_fft", f_max=8000)

    for i in [512, 1024, 2048, 4096]:
        for window in ['hann', 'hamming', 'blackman']:
            spectogram_plot(file1_fs, file1_data, f"cancion1_espectograma_{window}_{i:04d}", N=i, win=window)
            spectogram_plot(file2_fs, file2_data, f"cancion2_espectograma_{window}_{i:04d}", t=6, N=i, win=window)

time_domain()
freq_domain()
