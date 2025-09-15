import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from utils import *

a4_flauta_file_path    = 'data/a4_flauta.wav'
a4_clarinete_file_path = 'data/a4_clarinete.wav'
a4_violin_file_path    = 'data/a4_violin.wav'

a4_flauta_fs, a4_flauta_data = wavfile.read(a4_flauta_file_path)
a4_clarinete_fs, a4_clarinete_data = wavfile.read(a4_clarinete_file_path)
a4_violin_fs, a4_violin_data = wavfile.read(a4_violin_file_path)

## grafico completo
fig, ax = plot(a4_flauta_fs, a4_flauta_data, t_start=0.25, t_width=0.010)
save_plot(fig, a4_flauta_file_path)

fig, ax = plot(a4_clarinete_fs, a4_clarinete_data, t_start=0.25, t_width=0.010)
save_plot(fig, a4_clarinete_file_path)

fig, ax = plot(a4_violin_fs, a4_violin_data, t_start=0.25, t_width=0.010)
save_plot(fig, a4_violin_file_path)
