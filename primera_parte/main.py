import matplotlib.pyplot as plt

from numpy import arange
from scipy.io import wavfile

file_names = ['InASentimentalMood.wav', 'Zombie.wav']

def plot_wav_data(time, data, file_name):
    figure_title = 'Gráfico de `' + str(file_name) + '` en dominio de tiempo'

    new_figure = plt.figure(num=figure_title, figsize=(12, 6))
    plt.plot(time, data, label='Señal de Audio')
    plt.title(figure_title)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.legend()

    return new_figure

figures = []
for i, file_name in enumerate(file_names):
    sample_rate, data = wavfile.read(file_name)

    if len(data.shape) > 1:
        data = data[:, 0]

    time = arange(len(data)) / sample_rate
    figures.append(plot_wav_data(time, data, file_name))
    figures[i].show()

plt.show()
