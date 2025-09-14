import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from utils import plot, save_plot

file1_path          = 'data/cancion1.wav'
file2_path          = 'data/cancion2.wav'
filter1_h_file_path = 'data/respuesta_impulso_1.txt'
filter2_h_file_path = 'data/respuesta_impulso_2.txt'

file1_fs, file1_data = wavfile.read(file1_path)
file2_fs, file2_data = wavfile.read(file2_path)

filter1_h = np.loadtxt(filter1_h_file_path)
filter2_h = np.loadtxt(filter2_h_file_path)

# 'cancion1'
print(f'"{file1_path}", {file1_fs} Hz')

## grafico completo
plot(file1_fs, file1_data, file1_path)

## porciones cuasi-periodicas 'cancion1'
plot(file1_fs, file1_data, file1_path,
           t_start=0.248, t_width=0.008, a=0.24978, da=0.003)

plot(file1_fs, file1_data, file1_path,
           t_start=0.520, t_width=0.008, a=0.5208, da=0.003)

## salida de filtro 'cancion1'
file1_filter1_output = np.convolve(file1_data, filter1_h, mode='full')
file1_filter2_output = np.convolve(file1_data, filter2_h, mode='full')

fig, ax = plot(file1_fs, file1_filter1_output)
save_plot(fig, file1_path, extra_name="_filter1_output")

fig, ax = plot(file1_fs, file1_filter2_output)
save_plot(fig, file1_path, extra_name="_filter2_output")

# 'cancion2'
print(f'"{file2_path}", {file2_fs} Hz')

## grafico completo
plot(file2_fs, file2_data, file2_path, t_start=6)

## porciones cuasi-periodicas 'cancion2'
plot(file2_fs, file2_data, file2_path, t_start=14.720, t_width=0.01)
plot(file2_fs, file2_data, file2_path, t_start=26.570, t_width=0.01)

## salida de filtro 'cancion2'
file2_filter1_output = np.convolve(file2_data, filter1_h, mode='full')
file2_filter2_output = np.convolve(file2_data, filter2_h, mode='full')

fig, ax = plot(file2_fs, file2_filter1_output, t_start=6)
save_plot(fig, file2_path, t_start=6, extra_name="_filter1_output")

fig, ax = plot(file2_fs, file2_filter2_output, t_start=6)
save_plot(fig, file2_path, t_start=6, extra_name="_filter2_output")
