import serial
import numpy as np
import time

class RLCSampler:
    def __init__(self, puerto="COM3", baudios=460800, timeout=5):
        self.puerto = puerto
        self.baudios = baudios
        self.timeout_captura = timeout
        self.ser = None

    def conectar(self):
        """Conecta al puerto serial del ESP32 con validaciones."""
        try:
            self.ser = serial.Serial(self.puerto, self.baudios, timeout=1)
            time.sleep(0.5)  # Espera a que ESP32 esté listo
            print(f"SConectado a {self.puerto}")
        except serial.SerialException as e:
            raise ConnectionError(f"No se pudo conectar a {self.puerto}: {e}")

    def _validar_conexion(self):
        """Valida que exista una conexión activa."""
        if self.ser is None or not self.ser.is_open:
            raise RuntimeError("No hay conexión serial. Ejecute conectar() primero.")

    def _enviar_comando(self, comando):
        """Envía un comando al ESP32 y devuelve la respuesta inicial."""
        self._validar_conexion()
        self.ser.write(comando.encode())
        time.sleep(0.05)
        return self.ser.readline().decode(errors="ignore").strip()

    def generar_escalon(self, duracion=0.05, pre_delay=0.1, post_delay=0.2):
        """Pide al ESP32 que active el MOSFET y genere un escalón de entrada."""
        comando = f"STEP {int(duracion*1000)} {int(pre_delay*1000)} {int(post_delay*1000)}\n"
        respuesta = self._enviar_comando(comando)
        if respuesta and respuesta.upper() not in {"OK", "READY", "STEP"}:
            print(f"Respuesta inesperada del ESP32 al generar escalón: {respuesta}")
        return respuesta

    def capturar_paso(self, duracion=0.05, pre_delay=0.1, post_delay=0.2, max_intentos=3):
        """
        Captura datos mientras el ESP32 genera un escalón con el MOSFET.

        Args:
            duracion: Duración del escalón en segundos.
            pre_delay: Tiempo antes de iniciar el escalón en segundos.
            post_delay: Tiempo después del escalón en segundos.
            max_intentos: Errores de conversión permitidos.

        Returns:
            np.array: Voltajes en voltios (sin filtrar)
        """
        self._validar_conexion()

        datos_raw = []
        inicio = time.time()
        intentos = 0

        try:
            # Solicita al ESP32 la captura del escalón
            comando = f"CAPTURAR_ESCALON {int(duracion*1000)} {int(pre_delay*1000)} {int(post_delay*1000)}\n"
            self.ser.write(comando.encode())
            time.sleep(0.05)

            # Lee datos con timeout
            while time.time() - inicio < self.timeout_captura:
                linea = self.ser.readline().decode(errors="ignore").strip()
                if not linea:
                    continue

                if linea == "FIN":
                    break

                if linea and linea.isdigit():
                    try:
                        valor = int(linea)
                        # Valida que el valor esté en rango ADC (0-4095)
                        if 0 <= valor <= 4095:
                            datos_raw.append(valor)
                        else:
                            print(f"Valor fuera de rango: {valor}")
                    except ValueError:
                        intentos += 1
                        if intentos >= max_intentos:
                            raise ValueError(f"Demasiados errores de conversión (>{max_intentos})")
                        continue
                else:
                    # Posible línea de estado del ESP32
                    print(f"ℹESP32: {linea}")

            if not datos_raw:
                raise ValueError("No se capturaron datos válidos del ESP32")

            if len(datos_raw) < 10:
                raise ValueError(f"Muy pocos datos capturados: {len(datos_raw)} (mínimo 10)")

            # Conversión a voltios (rango 0-3.3V para ADC 12-bit)
            v_data = np.array(datos_raw) * (3.3 / 4095.0)

            print(f"Captura de escalón exitosa: {len(v_data)} muestras ({v_data.min():.2f}V - {v_data.max():.2f}V)")
            return v_data

        except (serial.SerialException, OSError) as e:
            raise RuntimeError(f"Error de puerto serial durante captura: {e}")


    def desconectar(self):
        """Cierra la conexión serial."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Desconectado")
