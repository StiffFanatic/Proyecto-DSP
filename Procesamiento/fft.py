import numpy as np

class FFTAnalyzer:
    def __init__(self, fs):
        self.fs = fs

    def compute_fft(self, y, window=True):
        y = np.asarray(y)
        N = len(y)

        if N == 0:
            raise ValueError("Señal vacía")

        if window:
            y = y * np.hanning(N)

        Y = np.fft.fft(y)
        freqs = np.fft.fftfreq(N, d=1 / self.fs)

        idx = freqs >= 0
        return freqs[idx], np.abs(Y[idx]) / N

    def dominant_frequency(self, y):
        freqs, mag = self.compute_fft(y)
        idx_max = np.argmax(mag[1:]) + 1
        return freqs[idx_max], mag[idx_max]