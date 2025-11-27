from utils import *
from data import *

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


