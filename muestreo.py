import serial
import serial.tools.list_ports

import numpy as np
import time


class RLCSampler:
    def __init__(self, puerto=None, baudios=460800, timeout=5):
        #print(self.puerto)
        self.puerto = puerto
        self.baudios = baudios
        self.timeout_captura = timeout
        self.ser = None
        self.datos_raw = []

    def conectar(self):
        #revisa en todos los puertos del pc
        puertos = [p.device for p in serial.tools.list_ports.comports()]
        self.puerto = self.puerto or (puertos[0] if puertos else None)
        print(f"Puerto: {self.puerto}")
        self.ser = serial.Serial(self.puerto, self.baudios, timeout=1)
        time.sleep(0.3)  # estabilización ESP32

    def cerrar(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def filtro_media_movil(self, data, n):
        if n <= 1:
            return data
        return np.convolve(data, np.ones(n) / n, mode='same')

    def _validar_conexion(self):
        if self.ser is None or not self.ser.is_open:
            raise RuntimeError("Puerto serial no conectado")

   
    def capturar(self, n_filtro=20):
        self._validar_conexion()
        self.datos_raw = []

        self.ser.write(b"INICIAR\n")

        while True:
            linea = self.ser.readline().decode(errors="ignore").strip()
            if linea == "FIN":
                break
            if linea.isdigit():
                self.datos_raw.append(int(linea))

        if not self.datos_raw:
            raise RuntimeError("No se recibieron datos")

        v_data = np.array(self.datos_raw) * (3.3 / 4095.0)
        v_filtrado = self.filtro_media_movil(v_data, n_filtro)
        t = np.linspace(0, 0.1, len(v_data))

        return t, v_data, v_filtrado

    def capturar_paso(self, duracion=0.05, pre_delay=0.1, post_delay=0.2):
        print("🟢 capturar_paso EJECUTÁNDOSE")
        """
        Captura la respuesta al escalón del circuito RLC.
        Retorna solo el voltaje (sin filtrar).
        """
        self._validar_conexion()
        self.datos_raw = []
        self.ser.write(b"INICIAR\n")

        comando = f"INICIAR {int(duracion*1000)} {int(pre_delay*1000)} {int(post_delay*1000)}\n"
        self.ser.write(comando.encode())
        time.sleep(0.05)

        inicio = time.time()

        print("📤 Enviando comando:", comando)
        while time.time() - inicio < self.timeout_captura:
            print("⏳ Esperando datos...")
            linea = self.ser.readline().decode(errors="ignore").strip()

            if not linea:
                continue

            if linea == "FIN":
                break

            if linea.isdigit():
                valor = int(linea)
                if 0 <= valor <= 4095:
                    self.datos_raw.append(valor)

        if len(self.datos_raw) < 10:
            raise RuntimeError("Datos insuficientes para análisis")

        v_data = np.array(self.datos_raw) * (3.3 / 4095.0)
        return v_data