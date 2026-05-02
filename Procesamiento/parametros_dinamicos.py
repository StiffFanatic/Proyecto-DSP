import numpy as np

class SystemIdentifier:
    def __init__(self, t, y):
        self.t = t
        self.y = y

    def estimate_second_order(self):
        if len(self.y) == 0 or len(self.t) == 0:
            raise ValueError("La señal está vacía y no puede ser analizada.")

        y_final = np.mean(self.y[-50:])
        y_peak = np.max(self.y)
        t_peak = self.t[np.argmax(self.y)]

        if y_final == 0:
            raise ValueError("No se puede calcular la sobreoscilación con valor final cero.")

        Mp = (y_peak - y_final) / y_final
        if Mp <= 0:
            raise ValueError("La señal no presenta una sobreoscilación válida para estimación.")

        try:
            log_mp = np.log(Mp)
            zeta = np.sqrt((log_mp**2) / (np.pi**2 + log_mp**2))
            if zeta >= 1:
                raise ValueError("El sistema no es subamortiguado.")
            wn = np.pi / (t_peak * np.sqrt(1 - zeta**2))
        except Exception as e:
            raise ValueError("No se pudo estimar un sistema subamortiguado válido.") from e

        return {
            "zeta": zeta,
            "wn": wn,
            "Mp": Mp,
            "t_peak": t_peak
        }