from scipy.io import wavfile
import numpy as np
import librosa
import os

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

for filename in os.listdir(canciones_dataset_dir):
    filename = canciones_dataset_dir + filename
    print(filename)
    file_data, file_fs = librosa.load(data_dir + filename, sr=None, mono=True)
    canciones_dataset.append(file_data)
    file_fs = int(file_fs)
