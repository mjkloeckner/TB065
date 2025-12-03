from utils import *
from scipy.signal import firwin, freqz, tf2zpk, get_window
from scipy.fft import fftshift
from scipy.io.wavfile import write as write_wav
import random

import pickle
database_name = 'database.pkl'

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

def comparacion_de_espectrogramas_filtrado_vs_original(h):
    for i, cancion in enumerate(canciones_dataset):
        spectrogram_plot(cancion.fs, cancion.data,
                        f'{cancion.name}_espectrograma_original_44100Hz',
                        N=1024, ylim=[0, 20000])

        filter_output = np.convolve(cancion.data, h, mode='same')
        spectrogram_plot(cancion.fs, filter_output,
                        f'{cancion.name}_espectrograma_filtrado_{cutoff}Hz',
                        N=1024, ylim=[0, 20000])

        spectrogram_plot(cancion.fs, filter_output,
                        f'{cancion.name}_espectrograma_filtrado_{cutoff}Hz_ylim_3000Hz_inferno',
                        cmap='inferno', ylim=[0, 3000], N=4096, win='hamming')

def generar_base_de_datos():
    h, fs = filtro_fir_deducido()

    DB = {
        'hash_nbits': 20,      # Cantidad de bits de los hashes
        'n_entries': 20,       # Cantidad de columnas de la tabla
        'ID_nbits': 12,        # Cantidad de bits para ID numérico de la canción
        'tabla': np.zeros((2 ** 20, 20), dtype=np.uint32)
    }

    for i, cancion in enumerate(canciones_dataset):
        data_filtered = np.convolve(cancion.data, h, mode='same')

        # Sxx es la matriz de energía donde el eje `y` es frecuencia (m) y
        # el eje `x` es tiempo (n).
        #
        # `nperseg`  tamaño de ventana (número de muestras por segmento)
        # `noverlap` cantidad de solapamiento entre ventanas
        f, t, E = spectrogram(data_filtered, fs=cancion.fs,
                nperseg=1024, noverlap=24, window='hamm')

        # E.shape retorna (num_bandas, num_frames) -> (m, n)
        # num_bandas, num_frames = E.shape
        # E = obtener_caracteristicas(E)

        H = generar_huella(E, fs)

        # if i == 0:
        #     graficar_huella(H, f'{cancion.name}_huella_acustica_completa')

        # graficar_huella(H, f'{cancion.name}_huella_acustica', xlim=[0, 100])
        DB = guardar_huella(i, H, DB)

    with open(f'{database_name}', 'wb') as f:
        pickle.dump(DB, f)

    print(f'[LOG] Base de datos guardada en `./{database_name}`')
    return DB

def generar_base_de_datos_si_no_existe():
    if os.path.exists(database_name):
        print(f'[LOG] Base de datos ya existe en `./{database_name}`, pasando...')
        try:
            with open(database_name, 'rb') as db_file:
                DB = pickle.load(db_file)

            print(f"[LOG] Se cargaron los archivos de `{database_name}`")

        except FileNotFoundError:
            print(f"[ERROR] No se encontro el archivo `{database_name}`")
        except EOFError:
            print(f"[ERROR] El archivo `{database_name}` puede estar incompleto o corrupto")
        except Exception as e:
            print(f"[ERROR] Ocurrio un error inesperado: {e}")
    else:
        cargar_canciones_dataset()
        DB = generar_base_de_datos()

    return DB

# calcula la matriz de características dado un espectrograma `E`
def obtener_caracteristicas(E):
    bandas_totales = 21  # Número de bandas de frecuencia (M)
    f_min = 300          # Frecuencia inferior de la primera banda (300 Hz)
    f_max = 2000         # Frecuencia superior de la última banda (2 kHz)

    num_bandas, num_frames = E.shape

    # La matriz F tendrá una fila menos (m+1 en E) y una columna menos (n-1 en E)
    # num_bandas_F = num_bandas - 1 (para evitar el desbordamiento de m+1)
    # num_frames_F = num_frames - 1 (para evitar el desbordamiento de n-1)
    F = np.zeros((num_bandas - 1, num_frames - 1), dtype=int)

    # Se itera sobre todas las bandas y frames que permiten la comparación
    for n in range(1, num_frames):      # n: tiempo (frame actual)
        for m in range(num_bandas - 1): # m: banda
            # Diferencia de energía entre banda m y m+1 en el tiempo 'n'
            diff_actual = E[m, n] - E[m + 1, n]

            # Frame anterior 'n-1'
            # Diferencia de energía entre banda m y m+1 en el tiempo 'n-1'
            diff_anterior = E[m, n - 1] - E[m + 1, n - 1]

            # Lógica de la Función Signo F(m, n)
            if diff_actual > diff_anterior:
                F[m, n - 1] = 1 # Se mapea n al índice correcto de la matriz F
            else:
                F[m, n - 1] = 0

    return F

def dividir_en_bandas_logaritmicas(Sxx, fs, n_bandas, fmin, fmax):
    # crear la matriz de filtros logarítmicos (Mel)
    # `n_fft` para librosa, debe ser el doble del número de filas de frecuencia
    # menos 2
    n_fft_librosa = (Sxx.shape[0] - 1) * 2

    mel_basis = librosa.filters.mel(
        sr=fs,
        n_fft=n_fft_librosa,
        n_mels=n_bandas,
        fmin=fmin,
        fmax=fmax)

    # multiplicar la matriz de filtros por el espectrograma de potencia
    # E_banda tendrá dimensiones (21 bandas, N_FRAMES) -> E(m, n)
    E_banda = np.dot(mel_basis, Sxx)

    # convertir la energía de las bandas a dB para aplicar la función F(m, n)
    # F(m,n) debe operar sobre la energía en dB para ser robusta.
    # se usa la referencia absoluta (ref=1.0) para que 0dB sea el nivel absoluto.
    E_db = librosa.power_to_db(E_banda, ref=1.0)
    return E_db


def generar_huella(E, fs):
    E_db = dividir_en_bandas_logaritmicas(E, fs, 21, 300, 2000)

    # E_db tiene dimensiones (m, n) -> (n_bandas, n_frames)
    num_bandas, num_frames = E_db.shape

    # La huella H(m, n) tendrá dimensiones (n_bandas - 1, n_frames - 1)
    H = np.zeros((num_bandas - 1, num_frames - 1), dtype=int)

    # n: tiempo (frame), m: banda
    for n in range(1, num_frames):    # n: empieza en 1 (segundo frame)
        for m in range(num_bandas - 1): # m: va de la primera hasta la penúltima banda
            diff_actual = E_db[m, n] - E_db[m + 1, n]
            diff_anterior = E_db[m, n - 1] - E_db[m + 1, n - 1]

            if diff_actual > diff_anterior:
                H[m, n - 1] = 1 # Se mapea n-1 al índice de la matriz H
            else:
                H[m, n - 1] = 0

    return H

def graficar_huella(H, save_name="", xlim=[], ylim=[], save_dir=""):
    fig, axis = plt.subplots(figsize=(8, 4))
    plt.pcolormesh(H, shading='auto', cmap='binary')

    # plt.title('Huella Digital Acústica H(m, n)')
    plt.ylabel('Diferencia de Banda Logarítmica')
    plt.xlabel('Frame de Tiempo')
    # plt.colorbar(ticks=[0, 1], label='Valor de H(m, n)')
    plt.gca().invert_yaxis() # invertir el eje y para que la frecuencia baja esté abajo
    plt.tight_layout()

    if len(xlim) != 0:
        plt.xlim(xlim)

    if len(ylim) != 0:
        plt.ylim(ylim)

    if save_name == "":
        plt.show()
    else:
        save_plot(fig, save_name, save_dir=save_dir)

def guardar_huella(ID, huella, DB):
    """
    Guarda la huella digital acústica 'huella' en la tabla hash de la estructura
    DB, identificando la canción con el identificador numérico.

    Parámetros
    ----------
    ID : int
        Identificador numérico del tema que corresponde a esta huella.
    huella : np.ndarray
        Huella acústica en forma de matriz binaria (unos y ceros).
    DB : dict
        Estructura con los siguientes campos:
            - 'hash_nbits': número de bits para el hash
            - 'n_entries': número de columnas de la tabla
            - 'ID_nbits': número de bits para guardar ID numérico de la canción
            - 'tabla': tabla hash de tamaño (2**hash_nbits, n_entries)

    Retorna
    -------
    DB : dict
        Estructura con tabla hash actualizada.
    """

    # Verificamos que huella sea una matriz binaria
    if not np.all((huella == 0) | (huella == 1)):
        raise ValueError("La matriz HUELLA contiene elementos no binarios")

    # Verificamos que huella tenga hash_nbits filas
    if huella.shape[0] != DB['hash_nbits']:
        raise ValueError(
            f"La matriz HUELLA tiene {huella.shape[0]} filas en lugar de {DB['hash_nbits']}"
        )

    # Generamos el elemento val a guardar, concatenando los bits del ID con los
    # bits del tiempo de cada frame
    frames_nbits = 32 - DB['ID_nbits']
    frames = np.mod(np.arange(1, huella.shape[1] + 1), 2 ** frames_nbits)
    val = np.uint32(ID + (2 ** DB['ID_nbits']) * frames)

    # Obtenemos las filas a guardar en la tabla, pasando las características de binario a decimal
    # (bi2de en MATLAB toma bits por fila; aquí usamos huella.T para el mismo comportamiento)
    hash_vals = np.dot(huella.T, 1 << np.arange(huella.shape[0])) + 1  # +1 por índices base 1

    # Primero grabamos en las filas en que queda espacio
    tabla = DB['tabla']
    fila_ok = tabla[hash_vals - 1, -1] == 0  # Filas que tienen espacio al final
    hash_ok = hash_vals[fila_ok]

    # Cantidad de elementos no nulos por fila
    count_nonzero = np.sum(tabla[hash_ok - 1, :] != 0, axis=1)
    indices = (hash_ok - 1, count_nonzero)  # (fila, columna disponible)
    tabla[indices] = val[fila_ok]

    # Finalmente grabamos en las filas que están llenas, pisando algún valor anterior al azar
    hash_col = hash_vals[~fila_ok]
    if len(hash_col) > 0:
        idx_rand = np.ceil(np.random.rand(len(hash_col)) * DB['n_entries']).astype(int) - 1
        tabla[hash_col - 1, idx_rand] = val[~fila_ok]

    DB['tabla'] = tabla
    return DB

def query_DB(DB, huella):
    """
    Hace un query a la base de datos para obtener el ID de las canciones
    coincidentes con la huella. Devuelve los 5 primeros resultados que mejor
    coinciden, ordenados en orden de prioridad descendente.

    Parámetros
    ----------
    DB : dict
        Estructura con los siguientes campos:
            - 'hash_nbits': número de bits para el hash
            - 'n_entries': número de columnas de la tabla
            - 'ID_nbits': número de bits para guardar ID numérico de la canción
            - 'tabla': tabla hash (np.ndarray de tamaño [2**hash_nbits, n_entries])
    huella : np.ndarray
        Huella acústica binaria (matriz de 0s y 1s)

    Retorna
    -------
    ID : np.ndarray
        Identificadores numéricos de los primeros 5 resultados que matchean
    MATCHES : np.ndarray
        Número de matches que tuvo cada ID
    """

    # Verificamos que HUELLA sea una matriz binaria
    if not np.all((huella == 0) | (huella == 1)):
        raise ValueError("La matriz HUELLA contiene elementos no binarios")

    # Verificamos que HUELLA tenga hash_nbits filas
    if huella.shape[0] != DB['hash_nbits']:
        raise ValueError(
            f"La matriz HUELLA tiene {huella.shape[0]} filas en lugar de {DB['hash_nbits']}"
        )

    # Obtenemos las filas a buscar en la tabla (binario → decimal)
    hash_vals = np.dot(huella.T, 1 << np.arange(huella.shape[0])) + 1  # +1 por índice MATLAB base 1

    # Extraemos los elementos de la tabla que corresponden a los hashes dados
    vals = DB['tabla'][hash_vals - 1, :]   # restamos 1 para índice base 0
    vals = vals[vals != 0]

    # Si todos los elementos eran nulos, devolvemos ceros
    if vals.size == 0:
        return np.array([0], dtype=np.uint32), np.array([0], dtype=np.uint32)

    # Extraemos de cada elemento el ID numérico y su frame
    ID1 = np.mod(vals, 2 ** DB['ID_nbits'])
    frames = np.floor_divide(vals, 2 ** DB['ID_nbits'])

    # Filtrado temporal: para cada ID, contamos coincidencias dentro del frame_span
    frame_span = huella.shape[1]
    unique_IDs = np.unique(ID1)
    MATCHES = np.zeros(len(unique_IDs), dtype=int)

    for k, uid in enumerate(unique_IDs):
        frame_aux = frames[ID1 == uid]
        matches = 0
        for k2 in range(len(frame_aux)):
            # Número de matches en intervalo frame_span
            match_aux = np.count_nonzero(
                (frame_aux >= frame_aux[k2]) &
                (frame_aux <= frame_aux[k2] + frame_span)
            )
            if match_aux > matches:
                matches = match_aux
        MATCHES[k] = matches

    # Ordenar por número de coincidencias en orden descendente
    idx = np.argsort(-MATCHES)  # orden descendente
    MATCHES = MATCHES[idx]
    unique_IDs = unique_IDs[idx]

    # Mantener solo los 5 primeros resultados
    Nm = min(5, len(unique_IDs))
    ID = unique_IDs[:Nm]
    MATCHES = MATCHES[:Nm]

    return ID.astype(np.uint32), MATCHES.astype(np.uint32)

def evaluar_cancion_raw(DB, cancion_data, cancion_fs, cancion_name):
    h, fs = filtro_fir_deducido()

    nro_pruebas = 0
    data = np.convolve(cancion_data, h, mode='same')
    print(f'[LOG] Evaluando cancion `{cancion_name}`')
    duracion_cancion = len(cancion_data) / cancion_fs
    print(f'[LOG] Duracion cancion: {duracion_cancion:05.02f}s')

    for r in range(0, 10):
        for T in [5, 10, 20]: # segmentso de 5, 10 y 20 segundos
            t_inicial = random.uniform(0.0, 1.0) * (duracion_cancion - 1.5*T)
            t_inicial = 0 if t_inicial < 0 else t_inicial
            print(f'[LOG] Intervalo {t_inicial:05.02f}:{t_inicial+T:05.02f}s', end='')
            f, t, E = generate_spectrogram(cancion_fs, data, t=t_inicial, dt=T)
            H = generar_huella(E, cancion_fs)

            nro_pruebas += 1
            id, matches = query_DB(DB, H)
            print(f' mejor coincidencia: `{canciones_dataset[id[0]].name}`')

    print("")

def evaluar_cancion(DB, cancion):
    h, fs = filtro_fir_deducido()

    nro_pruebas = 0
    data = np.convolve(cancion.data, h, mode='same')
    print(f'[LOG] Evaluando cancion `{cancion.path}`')
    duracion_cancion = len(data) / cancion.fs
    print(f'[LOG] Duracion cancion: {duracion_cancion:05.02f}s')

    for r in range(0, 10):
        for T in [5, 10, 20]: # segmentso de 5, 10 y 20 segundos
            t_inicial = random.uniform(0.0, 1.0) * (duracion_cancion - 1.5*T)
            t_inicial = 0 if t_inicial < 0 else t_inicial
            print(f'[LOG] Intervalo {t_inicial:05.02f}:{t_inicial+T:05.02f}s', end='')
            f, t, E = generate_spectrogram(cancion.fs, data, t=t_inicial, dt=T)
            H = generar_huella(E, cancion.fs)

            nro_pruebas += 1
            id, matches = query_DB(DB, H)
            print(f' mejor coincidencia: `{canciones_dataset[id[0]].name}`')

    print("")

def agregar_ruido_a_cancion(data, sigma=0.1):
    ruido = np.random.normal(loc=0, scale=sigma, size=len(data))
    cancion_con_ruido = data + ruido
    cancion_con_ruido = np.clip(cancion_con_ruido, -1.0, 1.0)
    return cancion_con_ruido

def calcular_potencia_ruido(potencia_orig, snr_db):
    snr_lineal = 10**(snr_db / 10)
    potencia_ruido = potencia_orig / snr_lineal
    return potencia_ruido

def evaluar_aciertos_agregar_ruido(DB):
    h, fs = filtro_fir_deducido()

    incorrectos = 0
    nro_pruebas = 0

    for i, cancion in enumerate(canciones_dataset):
        lista_a_probar = []
        lista_a_probar.append(cancion)

        for snr_db in [0, 10, 20]:
            potencia_cancion = np.mean(cancion.data**2)
            potencia_ruido = calcular_potencia_ruido(potencia_cancion, snr_db)
            sigma_ruido = np.sqrt(potencia_ruido)
            data = agregar_ruido_a_cancion(cancion.data, sigma_ruido)
            name = cancion.name + f"_ruido_SNR_{snr_db}dB"
            lista_a_probar.append(SimpleNamespace(
                name=name,
                data=data,
                fs=cancion.fs))

        for T in [5, 10, 20]: # segmentso de 5, 10 y 20 segundos
            duracion_cancion = len(cancion.data) / cancion.fs
            print(f'[LOG] Duracion cancion: {duracion_cancion:05.02f}s')

            t_inicial = random.uniform(0.0, 1.0) * (duracion_cancion - 1.5*T)
            t_inicial = 0 if t_inicial < 0 else t_inicial
            print(f'[LOG] Intervalo {T:05.02f}s {t_inicial:05.02f}:{t_inicial+T:05.02f}s')

            for elemento in lista_a_probar:
                data = np.convolve(elemento.data, h, mode='same')
                print(f'[LOG] Evaluando cancion `{elemento.name}`', end='')

                f, t, E = generate_spectrogram(elemento.fs, elemento.data, t=t_inicial, dt=T)
                H = generar_huella(E, elemento.fs)

                nro_pruebas += 1
                id, matches = query_DB(DB, H)
                print(f' mejor coincidencia: `{canciones_dataset[id[0]].name}`')
                if id[0] != i:
                    incorrectos += 1

        print("")


    print(f'[LOG] cantidad de pruebas incorrectas: {incorrectos} de {nro_pruebas}')
    print(f'[LOG] error porcentual: {(incorrectos/nro_pruebas)*100:0.02f}%')


def evaluar_aciertos(DB):
    h, fs = filtro_fir_deducido()

    incorrectos = 0
    nro_pruebas = 0
    for i, cancion in enumerate(canciones_dataset):
        data = np.convolve(cancion.data, h, mode='same')
        print(f'[LOG] Evaluando cancion `{cancion.path}`')
        duracion_cancion = len(data) / cancion.fs
        print(f'[LOG] Duracion cancion: {duracion_cancion:05.02f}s')
        for r in range(0, 5):
            for T in [5, 10, 20]: # segmentso de 5, 10 y 20 segundos
                t_inicial = random.uniform(0.0, 1.0) * (duracion_cancion - 1.5*T)
                t_inicial = 0 if t_inicial < 0 else t_inicial
                print(f'[LOG] Intervalo {t_inicial:05.02f}:{t_inicial+T:05.02f}s', end='')
                f, t, E = generate_spectrogram(cancion.fs, data, t=t_inicial, dt=T)
                H = generar_huella(E, cancion.fs)

                nro_pruebas += 1
                id, matches = query_DB(DB, H)

                print(f' mejor coincidencia: `{canciones_dataset[id[0]].name}`')
                if id[0] != i:
                    incorrectos += 1

        print("")

    print(f'[LOG] cantidad de pruebas incorrectas: {incorrectos} de {nro_pruebas}')
    print(f'[LOG] error porcentual: {(incorrectos/nro_pruebas)*100:0.02f}%')

