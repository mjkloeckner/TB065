from utils import *
from scipy.signal import firwin, freqz, tf2zpk, get_window
from scipy.fft import fftshift

############################# Tercera parte ###################################

cutoff = 2650    # frecuencia de corte
M = 700          # orden FIR (número de coeficientes)

def filtro_fir():
    fs = 44100

    # Diseño FIR pasabajos con ventana
    b = firwin(M, cutoff, fs=fs, window='hamming')

    w, H = freqz(b, worN=2048, fs=fs)
    fase = np.unwrap(np.angle(H))*180/np.pi

    fig, ax1, ax2 = freq_response_plot(w, H, fase, show=False)
    save_plot(fig, "respuesta_en_frecuencia_pasa-bajos_fir")

# `a` son los coeficientes de la respuesta al impulso (coinciden con los
# coeficientes de respuesta en frecuencia)
def filtro_fir_polos_y_ceros(a):
    zeros, poles, gain = tf2zpk(a, [1])

    # Crear figura
    fig, axis = plt.subplots(figsize=(8, 4))

    axis.scatter(np.real(zeros), np.imag(zeros),
                 s=25, facecolors='none', edgecolors='tab:blue', zorder=10,
                 label='Ceros', linewidth=1.25)

    axis.scatter(np.real(poles), np.imag(poles),
                 s=25, marker='x', color='tab:red',
                 label='Polos')

    axis.set_xlabel("Real", color="black")
    axis.set_ylabel("Imaginario", color="black")

    # Unidad círculo para referencia
    # theta = np.linspace(0, 2*np.pi, 100)
    # plt.plot(np.cos(theta), np.sin(theta))  # círculo unitario

    # axis.yaxis.set_major_locator(MaxNLocator(nbins=5))

    axis.grid(True, which='major', color='black', linestyle=':', linewidth=1.00)
    axis.grid(True, which='minor', color='black', linestyle=':', linewidth=0.50)
    axis.xaxis.set_minor_locator(AutoMinorLocator(2))

    plt.grid(True)
    plt.axis('equal')
    axis.legend()
    save_plot(fig, "polos_y_ceros_pasa-bajos_fir")


# a diferencia de la funcion `filtro_fir` se genera el filtro mediante
# operaciones elementales, como la multiplicacion por ventana, en lugar de usar
# una funcion de libreria externa como `firwin`
def filtro_fir_deducido():
    fs = 44100

    # respuesta ideal pasabajos: sinc centrada en M/2
    n = np.arange(M + 1)
    wc = 2*np.pi*cutoff / fs

    # h_ideal = sinc(wc*n)/(pi n); wc = 2pi*fc/fs
    # se normaliza la ganancia a 1 multiplicando por 2.0*(fc/fs)
    h_ideal = np.sinc(2.0 * (cutoff/fs) * (n - M/2))

    # ventana de hamming (de acuerdo a la formula de wikipedia)
    v_hamming = 0.54 - 0.46 * np.cos(2*np.pi*n/M)

    # respuesta del filtro FIR (version acotada de la sinc)
    h = h_ideal * v_hamming

    # se normaliza para tener ganancia unitaria para frecuancias <= fc
    h = h / np.sum(h)
    return h, fs

def filtro_fir_analisis(h, fs):
    fig, ax = dtime_plot(M, h, "respuesta_al_impulso_filtro_fir",
                         f'Respuesta al impulso filtro FIR grado {M}')

    # respuesta en frecuencia del filtro
    w, H = freqz(h, worN=2048, fs=fs)
    fase = np.unwrap(np.angle(H)) * 180 / np.pi

    fig, ax1, ax2 = freq_response_plot(w, H, fase, show=False, fc=5e3)
    save_plot(fig, "respuesta_en_frecuencia_pasa-bajos_fir")

    # polos y ceros
    filtro_fir_polos_y_ceros(h)

def filtro_fir_filtrar_comparar_espectogramas(h, data, fs):
    spectogram_plot(fs, data,
                    f"filtro_fir_espectograma_original_44100Hz",
                    N=1024, ylim=[0, 20000])

    filter_output = np.convolve(data, h, mode='same')
    spectogram_plot(fs, filter_output,
                    f"filtro_fir_espectograma_filtrada_{cutoff}Hz",
                    t=0, N=1024, ylim=[0, 20000])


def analisis_freq_ventanas():
    N = 1024

    v_rectangular = np.ones(N)
    v_hamming = np.hamming(N)

    # freq_plot(44100, v_hamming, "v_hamming_freq", f_max=2000, N=N*8)
    # freq_plot(44100, v_rectangular, "v_rectangular_freq", f_max=2000, N=N*8)

    v_rect_fft, _ = freq_compute_fft(44100, v_rectangular, N=N*8)
    v_hamm_fft, _ = freq_compute_fft(44100, v_hamming, N=N*8)

    # se centra el lobulo principal (frecuencia 0 en el centro del arreglo)
    v_rect_fft = fftshift(v_rect_fft)
    v_hamm_fft = fftshift(v_hamm_fft)

    v_rect_potencia = np.abs(v_rect_fft)**2
    v_hamm_potencia = np.abs(v_hamm_fft)**2

    # se agrega 1e-12 para evitar dividir por cero
    v_rect_potencia_db = 10 * np.log10(v_rect_potencia + 1e-12)
    v_hamm_potencia_db = 10 * np.log10(v_hamm_potencia + 1e-12)

    # Normalizar para que el pico del lóbulo principal sea 0 dB
    v_rect_potencia_db = v_rect_potencia_db - np.max(v_rect_potencia_db)
    v_hamm_potencia_db = v_hamm_potencia_db - np.max(v_hamm_potencia_db)

    # Gráfico de la Ventana Rectangular
    f = np.linspace(-0.5, 0.5, N*8)

    fig, ax = freq_graph_data_norm(f, v_rect_potencia_db,
                                   x_min=-0.04, x_max=0.04, y_min=-200, y_max=10,
                                   show=False)
    save_plot(fig, "potencia_db_espectro_ventana_rectangular")

    fig, ax = freq_graph_data_norm(f, v_hamm_potencia_db,
                                   x_min=-0.04, x_max=0.04, y_min=-200, y_max=10,
                                   show=False)
    save_plot(fig, "potencia_db_espectro_ventana_hamming")


    data_arr = [v_rect_potencia_db, v_hamm_potencia_db]
    leg_arr = ["Potencia espectro ventana rectangular",
               "Potencia espectro ventana Hamming"]

    fig, ax = freq_graph_multiple_data_norm(f, data_arr, leg_arr,
                                   x_min=-0.04, x_max=0.04, y_min=-100, y_max=40,
                                   show=False)

    save_plot(fig, "potencia_db_espectro_ventana_comparacion_hamming_rect")

    # plt.figure(figsize=(10, 6))
    # plt.plot(f, v_rect_potencia_db,
    #         label='Ventana Rectangular', linewidth=2, color='tab:blue')

    # Gráfico de la Ventana de Hamming
    # plt.plot(f, v_hamm_potencia_db,
    #         label='Ventana de Hamming', linewidth=2, color='tab:orange')

    # Enfocarse en el lóbulo principal
    # plt.xlim(-0.1, 0.1)

    # Configuración del Gráfico
    # plt.title('Comparación de Espectros de Potencia de Ventanas (Escala Logarítmica)')
    # plt.xlabel('Frecuencia Normalizada (f/Fs)')
    # plt.ylabel('Potencia Normalizada (dB)')

    # Limitar el eje Y para ver bien los lóbulos laterales
    # plt.ylim(-100, 5) 

    # Limitar el eje X para enfocarse en el lóbulo principal
    # plt.xlim(-0.1, 0.1) 

    # plt.grid(True, which="both", linestyle='--', alpha=0.7)
    # plt.legend()
    # plt.show()

    # freq_plot(44100, v_hamming_potencia, "v_hamming_potencia", f_max=20000, N=8192)
    # freq_plot(44100, v_rectangular_potencia, "v_rectangular_potencia", f_max=20000, N=8192)

    # interval_fft, interval_freqs = freq_compute_fft(fs, data, t, dt, N=N)
    # interval_fft, interval_freqs = freq_compute_fft(fs, data, t, dt, N=N)

    # f = np.linspace(-0.5, 0.5, n_fft)

    # filter_output = np.convolve(data, h, mode='same')

    # for i in [512, 1024, 2048]:
    #     # for window in ['boxcar', 'bartlett', 'hamming']:

    #     #     spectogram_plot(file1_fs, file_filter_output,
    #     #                     f"espectograma_submuestreado_{window}_{i:04d}", N=i,
    #     #                     win=window, ylim=[0, 3000], t=5, dt=1)

    #     N = 1024
    #     beta = 8.6
    #     kaiser_window = get_window(("kaiser", beta), N)
    #     spectogram_plot(canciones_dataset_common_fs, filter_output,
    #                     f"espectograma_submuestreado_kaiser_window_{i:04d}", N=i,
    #                     win=kaiser_window, ylim=[0, 3000], t=5, dt=1)
