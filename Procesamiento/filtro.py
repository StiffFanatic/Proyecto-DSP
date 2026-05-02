import numpy as np
from scipy.signal import butter, filtfilt

class SignalProcessor:
    def __init__(self, fs):
        self.fs = fs

    def lowpass(self, signal, fc=100):
        b, a = butter(4, fc / (self.fs / 2), btype='low')
        return filtfilt(b, a, signal)

    def normalize(self, signal):
        """Normaliza la señal dividiendo por el valor final (steady-state) para respuestas al escalón."""
        if len(signal) < 50:
            # Para señales cortas, usar el último valor
            y_final = signal[-1]
        else:
            # Usar el promedio de los últimos 50 puntos para el valor final
            y_final = np.mean(signal[-50:])
        
        if y_final == 0:
            # Si el valor final es cero, usar normalización por máximo absoluto
            return signal / np.max(np.abs(signal))
        else:
            # Normalizar por el valor final para que el steady-state sea 1.0
            return signal / y_final