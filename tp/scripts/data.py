from scipy.io import wavfile
import numpy as np
import librosa
import os
from types import SimpleNamespace

data_dir = '../data/'
plot_dir = '../plot/'
out_dir = '../out/'

## Datos
file1_path          = data_dir + 'cancion1.wav'
file2_path          = data_dir + 'cancion2.wav'
filter1_h_file_path = data_dir + 'respuesta_impulso_1.txt'
filter2_h_file_path = data_dir + 'respuesta_impulso_2.txt'

a4_flauta_file_path    = data_dir + 'a4_flauta.wav'
a4_clarinete_file_path = data_dir + 'a4_clarinete.wav'
a4_violin_file_path    = data_dir + 'a4_violin.wav'

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

## Datos tercera parte

# todas las canciones tienen formato mp3 y 44100Hz de frecuencia de muestreo
canciones_dataset_dir = data_dir + 'canciones/'
canciones_dataset = []
canciones_dataset_common_fs = 44100

i = 0
for i, file_name in enumerate(sorted(os.listdir(canciones_dataset_dir))):
    # if i > 3:
    #     break
    basename, ext = os.path.splitext(file_name)

    file_path = canciones_dataset_dir + file_name
    print("[LOG] Cargando '" + file_path + "'")

    file_data, file_fs = librosa.load(file_path, sr=None, mono=True)
    file_fs = int(file_fs)
    canciones_dataset.append(SimpleNamespace(
            name=basename,
            path=file_path,
            data=file_data,
            fs=file_fs))

print(f'[LOG] Se cargaron {i} archivos')
