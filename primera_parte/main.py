import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

file_names = ['InASentimentalMood.wav', 'Zombie.wav' ]

figures = []
for i in range(len(file_names)):
    file_name = file_names[i]

    sample_rate, data = wavfile.read(file_name)
    print("`" + str(file_name)+ "` tasa de muestreo: " + str(sample_rate) + " Hz")

    if len(data.shape) > 1:
        data = data[:, 0]

    time = np.arange(len(data)) / sample_rate

    figures.append(plt.figure(figsize=(12, 6)))
    plt.plot(time, data, label='Señal de Audio')
    title='Archivo `', file_name, '` en Función del Tiempo'
    plt.title('Archivo `%s` en Función del Tiempo' %file_name)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.legend()
    figures[i].show()

plt.show()
