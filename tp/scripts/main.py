import numpy as np

# archivos locales
from utils import *
from primera_parte import *
from segunda_parte import *
from tercera_parte import *
from data import *

############################# Llamados a funciones ############################

def primera_parte():
    # time_domain
    time_domain_cancion1()
    time_domain_cancion2()
    time_domain_music_instruments()

def segunda_parte():
    freq_domain
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

def tercera_parte():
    # h, fs = filtro_fir_deducido()

    # filtro_fir_analisis(h, fs)

    # for i in len(canciones_dataset):
    #     filtro_fir_filtrar_comparar_espectogramas(
    #             h, canciones_dataset[i], canciones_dataset_common_fs)

    # analisis_freq_ventanas()


# primera_parte()
# segunda_parte()
tercera_parte()
