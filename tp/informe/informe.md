# Trabajo Práctico

Señales y sistemas (TB065) - FIUBA  
Martin Klöckner - [mklockner@fi.uba.ar](mailto:mklockner@fi.uba.ar)  

\vspace{-0.50em}
\rule{\linewidth}{0.5pt}
\vspace{-1.00em}

En el presente trabajo se realiza un análisis visual en el dominio temporal de
dos señales musicales. Para realizar el análisis se utiliza un script de python
para graficar en principio las señales completas y luego porciones de ambas en
busca de intervalos particulares. Por ultimo se analiza el comportamiento de las
señales al aplicarse dos filtros diferentes, teniendo solo la respuesta al
impulso de los filtros.

## Primer muestra

Para la primer muestra (archivo `cancion1.wav`) se realiza el gráfico de la
misma en el dominio temporal, el resultado se muestra en la figura 1.

La frecuencia de muestreo de la misma es 44100 Hz, esto se obtiene del mismo
script utilizado para graficar el archivo, en el cual se divide la cantidad de
muestras por la duración del archivo.

\begin{figure}[H]
    \vspace{-1em}
    \centering
    \includegraphics[width=\linewidth]{../plot/cancion1.png}
    \caption{Gráfico de archivo 'cancion1.wav'}
    \vspace{-1em}
\end{figure}

### Secciones cuasi-periódicas

Cuando la señal tiene una estructura repetitiva, pero con variaciones en
amplitud, fase o frecuencia se dice que la señal es cuasi-periódica.

Realizando un análisis visual en detalle de la muestra se buscan partes donde se
comporte como tal, dos ejemplos se dan en las figuras 2 y 3. En la primera se
gráfica el intervalo $0.248$ s a $0.256$ s, mientras que en la segunda se
gráfica el intervalo $0.520$ s a $0.528$ s.

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{../plot/cancion1_0_248s_a_0_256s.png}
\caption{Sección cuasi-periódica archivo 'cancion.wav'}
\vspace{-1em}
\end{figure}

Dentro de los intervalos cuasi-periódicos graficados, se pueden detectar
visualmente los períodos fundamentales, los cuales se ven resaltados en color
celeste claro.

Curiosamente en ambos casos el período es igual y resulta $T=0.003$ s,
lo cual corresponde con una frecuencia de aproximadamente $333$ Hz. Comparando
con notas musicales de tabla esto se asemeja a una nota *E4*, la cual tiene una
frecuencia de $329.228$ Hz. Siendo que el período se relaciona de manera inversa
con la frecuencia y esta de manera directa con la nota musical, se puede
asegurar que al disminuir este período la frecuencia aumentará y la nota musical
será mas aguda, mientras que en el caso contrario si aumenta el período la
frecuencia disminuye y también la nota musical.

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{../plot/cancion1_0_52s_a_0_528s.png}
\caption{Sección cuasi-periódica archivo 'cancion.wav'}
\end{figure}

## Segunda muestra

<!-- De manera análoga a lo realizado para la primer muestra (archivo -->
<!-- `cancion1.wav`) se realiza para la segunda muestra (archivo `cancion2.wav`). -->

Utilizando el mismo script de python utilizado para la primer muestra (archivo
`cancion1.wav`) se gráfica la señal de la segunda muestra (correspondiente al
archivo `cancino2.wav`) en el dominio temporal, en este caso se gráfica a partir
del segundo 6 ya que antes de esto la señal tiene amplitud nula, con lo cual no
aporta información significativa, el gráfico resultante se muestra en la figura
4.

La frecuencia fundamental de esta segunda muestra resulta $48000$ Hz, esto
también se obtiene del script de python.

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{../plot/cancion2_6s.png}
\caption{Gráfico de archivo 'cancion2.wav'}
\end{figure}

### Secciones no-periódicas

A diferencia del análisis realizado sobre la primer muestra en busca de
secciones cuasi-periódicas, para esta segunda muestra se buscan secciones no
periódicas, esto es, secciones donde la señal no tiene un patron repetitivo
marcado. Se toman dos intervalos en los cuales la señal de muestra se
comporta como tal, el intervalo de $14.72$s a $14.73$s y el intervalo $26.57$s a
$26.58$s, ambos intervalos se muestran graficados en las figura 5 y 6
respectivamente.

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{../plot/cancion2_14_72s_a_14_73s.png}
\caption{Sección no periódica archivo 'cancion2.wav'}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{../plot/cancion2_26_57s_a_26_58s.png}
\caption{Sección no periódica archivo 'cancion2.wav'}
\end{figure}

Dado que las secciones son no periódicas, no se puede hablar de una frecuencia
fundamental como si se podía en las secciones cuasi-periódicas en la primer
muestra.

## Filtrado

Para obtener la salida de la señal luego de aplicarle un filtro (respuesta al
impulso del primer filtro correspondiente al archivo `respuesta_impulso_1.txt` y
del segundo filtro correspondiente al archivo `respuesta_impulso_2.txt`) es
necesario realizar una convolución entre la señal de entrada y la respuesta al
impulso del filtro, esto suponiendo que el filtro es un sistema LTI (si no lo
fuera no se podría calcular la salida solo teniendo la respuesta al impulso).

La salida del filtro 1 al aplicar la primer muestra se puede ver en la figura 7,
se puede ver que atenúa partes de la señal principalmente cerca del segundo
$7$ y también una parte cerca del segundo $8.75$.

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{../plot/cancion1_filter1_output.png}
\caption{Primer muestra salida de filtro 1}
\end{figure}

Aplicando el segundo filtro a la primer muestra resulta como se muestra e el
gráfico de figura 8. Se puede ver que esta a diferencia del filtro 1, no atenúa
o amplifica significativamente partes de la señal, si no que es más leve.

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{../plot/cancion1_filter2_output.png}
\caption{Primer muestra salida de filtro 2}
\end{figure}

De manera análoga para la segunda muestra se aplican los filtros mediante la
convolución entre la señal de muestra y la respuesta al impulso del respectivo
filtro. La salida de la segunda muestra al aplicar el primer y segundo filtro se
puede ver en las figuras 9 y 10 respectivamente.

Se puede ver claramente en la figura 9 y comparando con el gráfico de la muestra
original (figura 4) que se atenúa la señal principalmente en la primera parte de
la señal (antes del segundo $18.5$) aunque también ocurre en la segunda parte,
por ejemplo en el pico que ocurre cerca del segundo $24.5$, en la señal original
alcanza un máximo de $1.00$ mientras que en la señal filtrada se atenúa a
$0.75$.

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{../plot/cancion2_6s_filter1_output.png}
\caption{Segunda muestra salida filtro 1}
\end{figure}

\begin{figure}[H]
\centering
\includegraphics[width=\linewidth]{../plot/cancion2_6s_filter2_output.png}
\caption{Segunda muestra salida filtro 2}
\end{figure}

En el caso del segundo filtro, de manera análoga a lo que ocurría con la primer
muestra, no se observa un cambio significativo en la señal filtrada, si no mas
bien una leve atenuación general, aunque si se percibe una drástica atenuación
de un instante especifico de la señal en el segundo $29.9$ aproximadamente.
