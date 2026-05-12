import numpy as np


class FFT_analizador:
    def __init__(self, fs):
        self.fs = fs

    def fft_escalon(self, y, window=True, kernel=5):
        """
        FFT optimizada para respuesta al escalón.

        Pasos:
          1. Derivada discreta  → elimina componente DC del escalón
          2. Ventana de Hanning → reduce spectral leakage
          3. FFT                → espectro de frecuencia
          4. Suavizado móvil   → elimina picos espurios por ruido
        
        Retorna:
            freqs      : array de frecuencias (Hz), solo positivas
            mag        : magnitud FFT original (para graficar)
            mag_smooth : magnitud suavizada   (para detectar pico)
        """
        y = np.asarray(y, dtype=float)

        # 1. Derivada: convierte el escalón en transitorio puro, elimina DC
        dy = np.diff(y) * self.fs
        N = len(dy)

        if N == 0:
            raise ValueError("Señal vacía tras diferenciación")

        # 2. Ventana: reduce spectral leakage en los bordes
        if window:
            dy = dy * np.hanning(N)

        # 3. FFT
        Y = np.fft.fft(dy)
        freqs = np.fft.fftfreq(N, d=1/self.fs)

        idx   = freqs >= 0
        freqs = freqs[idx]
        mag   = np.abs(Y[idx]) / N

        # 4. Suavizado: promedio móvil para eliminar picos espurios
        mag_smooth = np.convolve(mag, np.ones(kernel) / kernel, mode='same')

        return freqs, mag, mag_smooth
