import tkinter as tk
import threading
import numpy as np
import os
import control as ctrl

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk

from Adquisición_de_datos import muestreo

# Módulos de procesamiento 
from Procesamiento.data import DataIO
from Procesamiento.filtro import SignalProcessor
from Procesamiento.parametros_dinamicos import SystemIdentifier
from Procesamiento.fdt import TransferFunctionEstimator
from Procesamiento.fft import FFTAnalyzer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "assets", "Imagenes", "usc.ico")
ICON_IMG_PATH = os.path.join(BASE_DIR, "assets", "Imagenes", "usc.ico")


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Proyecto DSP - Análisis de circuitos RLC")
        self.root.geometry("1100x600")

        print("ICON_PATH =", ICON_PATH)
        print("EXISTE =", os.path.exists(ICON_PATH))

        try:
            self.root.iconbitmap(ICON_PATH)
        except Exception as e:
            print(f"No se pudo cargar el icono: {e}")

        # ---------- PARÁMETROS ----------
        self.fs = 1000  
        self.v_raw = None
        self.G_est = None
        self.params = None
        self.rlc_params = None
        self.data_origen = None
        

        # ---------- OBJETOS ----------
        self.sampler = muestreo.RLCSampler()
        self.data_io = DataIO()
        self.processor = SignalProcessor(self.fs)
        self.fft_analyzer = FFTAnalyzer(self.fs)

        self._create_layout()
        self._create_plot()
        self.mostrar_funcion_canonica()

    # ---------- LAYOUT ----------
    def _create_layout(self):
        self.frame_left = tk.Frame(self.root, bg="#ecf0f1")
        self.frame_left.pack(side="left", fill="both", expand=True)

        self.frame_right = tk.Frame(self.root, bg="#bdc3c7", width=260)
        self.frame_right.pack(side="right", fill="y")

        tk.Label(
            self.frame_left,
            text="Análisis de circuitos RLC",
            font=("Segoe UI", 16, "bold"),
            bg="#ecf0f1"
        ).pack(pady=10)

        self.graph_frame = tk.Frame(self.frame_left, bg="white")
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.eq_frame = tk.Frame(self.frame_left, bg="#ecf0f1", height=80)
        self.eq_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            self.frame_right,
            text="Controles",
            font=("Segoe UI", 14, "bold"),
            bg="#bdc3c7"
        ).pack(pady=10)

        # Frame para parámetros en el panel derecho
        self.params_frame = tk.Frame(self.frame_right, bg="#ecf0f1")
        self.params_frame.pack(fill="x", padx=10, pady=10)

        # ---------- ICONO SUPERIOR DERECHO ----------
        try:
            img = Image.open(ICON_IMG_PATH)
            img = img.resize((70, 70), Image.LANCZOS)  # tamaño del icono
            self.icon_img = ImageTk.PhotoImage(img)

            self.icon_label = tk.Label(
                self.frame_left,
                image=self.icon_img,
                bg="#ecf0f1"
            )

            # Posicionar arriba a la derecha
            self.icon_label.place(relx=0.98, rely=0.02, anchor="ne")

        except Exception as e:
            print("Error cargando icono GUI:", e)

    # ---------- GRÁFICA ----------
    def _create_plot(self):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Respuesta del sistema")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Amplitud")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self._create_params_display()

    # ---------- PARÁMETROS DISPLAY ----------
    def _create_params_display(self):
        """Crea los labels para mostrar los parámetros del sistema."""
        # Título
        tk.Label(
            self.params_frame,
            text="Parámetros del Sistema",
            font=("Segoe UI", 12, "bold"),
            bg="#ecf0f1"
        ).pack(pady=(0, 10))

        # Frame para parámetros dinámicos
        dyn_frame = tk.Frame(self.params_frame, bg="#ecf0f1")
        dyn_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            dyn_frame,
            text="Dinámicos:",
            font=("Segoe UI", 10, "bold"),
            bg="#ecf0f1"
        ).pack(anchor="w")

        # Labels para parámetros dinámicos
        self.zeta_label = tk.Label(dyn_frame, text="ζ = --", font=("Consolas", 10), bg="#ecf0f1")
        self.zeta_label.pack(anchor="w", padx=10)

        self.wn_label = tk.Label(dyn_frame, text="ωn = -- rad/s", font=("Consolas", 10), bg="#ecf0f1")
        self.wn_label.pack(anchor="w", padx=10)

        self.mp_label = tk.Label(dyn_frame, text="Mp = --", font=("Consolas", 10), bg="#ecf0f1")
        self.mp_label.pack(anchor="w", padx=10)

        self.tp_label = tk.Label(dyn_frame, text="tp = -- s", font=("Consolas", 10), bg="#ecf0f1")
        self.tp_label.pack(anchor="w", padx=10)

        # Frame para parámetros RLC
        rlc_frame = tk.Frame(self.params_frame, bg="#ecf0f1")
        rlc_frame.pack(fill="x")

        tk.Label(
            rlc_frame,
            text="RLC (C=1μF):",
            font=("Segoe UI", 10, "bold"),
            bg="#ecf0f1"
        ).pack(anchor="w")

        # Labels para parámetros RLC
        self.r_label = tk.Label(rlc_frame, text="R = -- Ω", font=("Consolas", 10), bg="#ecf0f1")
        self.r_label.pack(anchor="w", padx=10)

        self.l_label = tk.Label(rlc_frame, text="L = -- mH", font=("Consolas", 10), bg="#ecf0f1")
        self.l_label.pack(anchor="w", padx=10)

        self.c_label = tk.Label(rlc_frame, text="C = -- μF", font=("Consolas", 10), bg="#ecf0f1")
        self.c_label.pack(anchor="w", padx=10)

    def plot_signal(self, y):
        self.ax.clear()
        t = np.linspace(0, len(y) / self.fs, len(y))
        self.ax.plot(t, y)
        self.ax.set_title("Señal")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Amplitud")
        self.ax.grid(True)
        self.canvas.draw()

    # ---------- FUNCIONES ----------
    def conectar_serial(self):
        try:
            self.sampler.conectar()
            print("Conectado al ESP32")
        except Exception as e:
            print("Error de conexión:", e)

    def capturar_escalon(self, duracion=0.05, pre_delay=0.1, post_delay=0.2):
        """Genera y captura la respuesta al escalón usando el MOSFET en el ESP32."""

        def tarea():
            print("Botón presionado, hilo iniciado")
            
            try:
                print("1️⃣ Entró al hilo")
                print("2️⃣ sampler =", self.sampler)
                # Captura desde el sampler (retorna voltajes en V)
                self.v_raw = self.sampler.capturar_paso(
                    duracion=duracion,
                    pre_delay=pre_delay,
                    post_delay=post_delay
                )

                print("3️⃣ Antes de capturar_paso")
                self.v_raw = self.sampler.capturar_paso()
                print("4️⃣ Después de capturar_paso")

                if self.v_raw is not None and len(self.v_raw) > 0:
                    print(f"Captura de escalón: {len(self.v_raw)} muestras")

                    # Tiempo total del experimento
                    t_total = pre_delay + duracion + post_delay

                    # Vector tiempo (uniforme para análisis DSP)
                    t = np.linspace(0, t_total, len(self.v_raw))

                    # Guardar datos
                    path = self.data_io.save(t, self.v_raw)
                    print(f"Datos guardados en: {path}")

                    # Limpiar parámetros anteriores
                    self.limpiar_parametros()

                    # Visualizar señal capturada
                    self.plot_signal(self.v_raw)

                    # Marcar origen de datos para FFT / análisis
                    self.data_origen = "serial"

            except Exception as e:
                import traceback
                traceback.print_exc()

        threading.Thread(target=tarea, daemon=True).start()

    def cargar_datos_prueba(self):
        """Carga datos de prueba desde archivo CSV existente."""
        try:
            import os
            data_folder = "results/data"
            
            # Buscar archivos de prueba
            if os.path.exists(data_folder):
                archivos_prueba = [f for f in os.listdir(data_folder) if f.startswith('rlc_data_test_')]
                if archivos_prueba:
                    # Usar el primer archivo encontrado (ordenado alfabéticamente)
                    archivo_prueba = sorted(archivos_prueba)[0]
                    path_completo = os.path.join(data_folder, archivo_prueba)
                    
                    # Cargar datos
                    t, v = self.data_io.load(path_completo)
                    self.v_raw = v
                    
                    print(f"   Datos de prueba cargados: {len(self.v_raw)} muestras desde {archivo_prueba}")
                    print(f"   Duración: {t[-1]:.3f} segundos")
                    print(f"   Fs efectiva: {len(self.v_raw)/(t[-1]-t[0]):.1f} Hz")
                    
                    # Limpiar parámetros anteriores
                    self.limpiar_parametros()
                    
                    # Visualizar datos en la gráfica
                    self.plot_signal(self.v_raw)

                    self.v_load = self.v_raw
                    self.data_origen = "archivo"

                else:
                    print("No se encontraron archivos de prueba. Ejecute 'python test_proyecto.py' primero.")
            else:
                print("Carpeta de datos no existe. Ejecute 'python test_proyecto.py' primero.")
                
        except Exception as e:
            print(f"Error cargando datos de prueba: {e}")

    def calcular_parametros_rlc(self, zeta, wn, C_asumido=1e-6):
        """
        Calcula R, L, C a partir de parámetros dinámicos.
        Asume un valor típico para C y calcula L y R.
        
        Args:
            zeta: Factor de amortiguamiento
            wn: Frecuencia natural (rad/s)
            C_asumido: Capacitancia asumida (F), default 1μF
            
        Returns:
            dict: {'R': resistencia, 'L': inductancia, 'C': capacitancia}
        """
        # Para circuito RLC serie:
        # ωn = 1/√(LC)  ⇒  LC = 1/ωn²
        # ζ = R/(2√(L/C))  ⇒  R = 2ζ√(L/C)
        
        # Calcular L a partir de LC = 1/ωn² y C asumido
        LC = 1 / (wn ** 2)
        L = LC / C_asumido
        
        # Calcular R a partir de ζ = R/(2√(L/C))
        sqrt_LC = np.sqrt(L / C_asumido)
        R = 2 * zeta * sqrt_LC
        
        return {
            'R': R,
            'L': L,
            'C': C_asumido
        }

    def actualizar_display_parametros(self):
        """Actualiza los labels de parámetros en la GUI."""
        if self.params is not None:
            # Actualizar parámetros dinámicos
            self.zeta_label.config(text=f"ζ = {self.params['zeta']:.4f}")
            self.wn_label.config(text=f"ωn = {self.params['wn']:.2f} rad/s")
            self.mp_label.config(text=f"Mp = {self.params['Mp']:.3f}")
            self.tp_label.config(text=f"tp = {self.params['t_peak']:.4f} s")

        if self.rlc_params is not None:
            # Actualizar parámetros RLC
            self.r_label.config(text=f"R = {self.rlc_params['R']:.1f} Ω")
            self.l_label.config(text=f"L = {self.rlc_params['L']*1000:.1f} mH")
            self.c_label.config(text=f"C = {self.rlc_params['C']*1e6:.0f} μF")

    def limpiar_parametros(self):
        """Limpia los parámetros mostrados en la GUI."""
        self.params = None
        self.rlc_params = None
        
        # Reset labels
        self.zeta_label.config(text="ζ = --")
        self.wn_label.config(text="ωn = -- rad/s")
        self.mp_label.config(text="Mp = --")
        self.tp_label.config(text="tp = -- s")
        self.r_label.config(text="R = -- Ω")
        self.l_label.config(text="L = -- mH")
        self.c_label.config(text="C = -- μF")

    def mostrar_analisis(self):
        if self.v_raw is None or len(self.v_raw) == 0:
            print(" No hay datos para analizar. Capture datos primero.")
            return

        t = np.linspace(0, len(self.v_raw) / self.fs, len(self.v_raw))

        try:
            # Preprocesamiento: Filtro Butterworth + Normalización
            y_filt = self.processor.lowpass(self.v_raw, fc=100)
            y_norm = self.processor.normalize(y_filt)
            
            print(" Filtrado exitoso (Butterworth lowpass, fc=100Hz)")

            # Identificación del sistema
            identifier = SystemIdentifier(t, y_norm)
            self.params = identifier.estimate_second_order()

            print("Parámetros estimados:")
            print(f"  ζ  = {self.params['zeta']:.3f}")
            print(f"  ωn = {self.params['wn']:.3f} rad/s")
            print(f"  Mp = {self.params['Mp']:.3f}")
            print(f"  tp = {self.params['t_peak']:.3f}s")

            # Calcular parámetros RLC
            rlc_params = self.calcular_parametros_rlc(
                self.params['zeta'], 
                self.params['wn']
            )
            self.rlc_params = rlc_params
            
            print(" Parámetros RLC calculados (C asumido = 1μF):")
            print(f"  R = {rlc_params['R']:.1f} Ω")
            print(f"  L = {rlc_params['L']*1000:.1f} mH")
            print(f"  C = {rlc_params['C']*1e6:.0f} μF")

            # Función de transferencia
            tf_est = TransferFunctionEstimator(
                self.params["zeta"],
                self.params["wn"]
            )
            self.G_est = tf_est.get_transfer_function()

            print("Función de transferencia estimada:")
            print(self.G_est)
            
            # Mostrar función de transferencia estimada en la ventana
            self._mostrar_funcion_transferencia_estimada(self.params["wn"], self.params["zeta"])
            
            # Visualizar la señal filtrada y normalizada
            self.plot_signal(y_norm)

            # Actualizar display de parámetros
            self.actualizar_display_parametros()
            
        except ValueError as e:
            print(f"Error en la estimación: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def simular(self):
        """Abre diálogo para ingresar R, L, C o usa estimación previa."""
        self._open_rlc_dialog()

    def _open_rlc_dialog(self):
        """Crea un diálogo para ingresar R, L, C."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Parámetros RLC")
        dialog.geometry("150x250")
        dialog.resizable(False, False)

        # Frame para inputs
        frame = tk.Frame(dialog, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # Resistencia (Ω)
        tk.Label(frame, text="R (Ω):", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5)
        entry_r = tk.Entry(frame, width=15)
        entry_r.insert(0, "50")
        entry_r.grid(row=0, column=1, pady=5)

        # Inductancia (H)
        tk.Label(frame, text="L (H):", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5)
        entry_l = tk.Entry(frame, width=15)
        entry_l.insert(0, "0.1")
        entry_l.grid(row=1, column=1, pady=5)

        # Capacitancia (F)
        tk.Label(frame, text="C (F):", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=5)
        entry_c = tk.Entry(frame, width=15)
        entry_c.insert(0, "10e-6")
        entry_c.grid(row=2, column=1, pady=5)

        # Botones
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        def simular_con_parametros():
            try:
                R = float(entry_r.get())
                L = float(entry_l.get())
                C = float(entry_c.get())
                
                if R <= 0 or L <= 0 or C <= 0:
                    raise ValueError("Los valores deben ser positivos")
                
                self._ejecutar_simulacion(R, L, C)
                dialog.destroy()
            except ValueError as e:
                print(f"Error en parámetros: {e}")

        tk.Button(btn_frame, text="Simular", command=simular_con_parametros, width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, width=10).pack(side="left", padx=5)

    def _ejecutar_simulacion(self, R, L, C):
        """Calcula y visualiza la función de transferencia RLC."""
        try:
            # Parámetros del sistema RLC
            # Para un circuito RLC serie: ωn = 1/√(LC), ζ = R/(2√(L/C))
            wn = 1 / np.sqrt(L * C)
            zeta = R / (2 * np.sqrt(L / C))
            
            print(f" Parámetros RLC ingresados:")
            print(f"  R = {R} Ω")
            print(f"  L = {L} H")
            print(f"  C = {C} F")
            print(f"  ωn = {wn:.3f} rad/s")
            print(f"  ζ = {zeta:.3f}")
            
            if zeta >= 1:
                tipo_resp = "críticamente amortiguado"
            else:
                tipo_resp = "subamortiguado"
            print(f"  Tipo: {tipo_resp}")
            
            # Crear función de transferencia teórica
            # G(s) = ωn² / (s² + 2ζωnS + ωn²)
            tf_teorica = TransferFunctionEstimator(zeta, wn).get_transfer_function()
            
            print(f"\nFunción de transferencia teórica:")
            print(tf_teorica)
            
            # Simular respuesta al escalón - Enfocarse en la respuesta transitoria
            # Usar tiempo más corto para ver mejor las oscilaciones
            t_sim = np.linspace(0, 0.5, 5000)
            t_resp, y_resp = ctrl.step_response(tf_teorica, t_sim)
            
            # Graficar mejorado
            self.ax.clear()
            
            # Gráfica principal
            self.ax.plot(t_resp, y_resp, 'b-', linewidth=2.5, label='Respuesta al escalón')
            
            # Línea de valor final
            self.ax.axhline(y=1, color='r', linestyle='--', linewidth=1.5, alpha=0.7, label='Valor final (1.0)')
            
            # Variables para zoom
            t_pico = None
            Mp = 0.0
            t_peak = 0.0
            
            # Si es subamortiguado, marcar el pico
            if zeta < 1:
                idx_pico = np.argmax(y_resp)
                t_pico = t_resp[idx_pico]
                y_pico = y_resp[idx_pico]
                Mp = (y_pico - 1) * 100.0  # Sobreoscilación en %
                t_peak = t_pico
                
                # Marcar pico
                self.ax.plot(t_pico, y_pico, 'r*', markersize=15, label=f'Pico: {y_pico:.3f} @ {t_pico:.3f}s')
                self.ax.axvline(x=t_pico, color='g', linestyle=':', alpha=0.5)
                
                print(f"  Pico máximo: {y_pico:.4f} en t={t_pico:.4f}s")
                print(f"  Sobreoscilación: {Mp:.2f}%")
            
            # Actualizar los parámetros de la GUI con la simulación
            self.params = {
                "zeta": zeta,
                "wn": wn,
                "Mp": Mp,
                "t_peak": t_peak
            }
            self.rlc_params = {
                "R": R,
                "L": L,
                "C": C
            }
            self.actualizar_display_parametros()
            
            # Formatting
            # self.ax.set_title(f"Sistema RLC: R={R}Ω | L={L}H | C={C}F | ζ={zeta:.4f} ({tipo_resp})"
            self.ax.set_title(f"Sistema RLC : ({tipo_resp})", 
                            fontsize=11, fontweight='bold', pad=10)
            self.ax.set_xlabel("Tiempo (s)", fontsize=10)
            self.ax.set_ylabel("Amplitud (V)", fontsize=10)
            self.ax.grid(True, alpha=0.4, linestyle='--', linewidth=0.7)
            self.ax.legend(loc='right', fontsize=9)
            
            # Zoom en la respuesta transitoria
            if t_pico is not None:
                t_max_mostrar = max(t_pico * 4, 0.1)
            else:
                t_max_mostrar = 0.5
            self.ax.set_xlim(0, t_max_mostrar)
            self.ax.set_ylim(min(y_resp) - 0.05, max(y_resp) + 0.15)
            
            self.canvas.draw()
            
            # Mostrar función de transferencia en la ventana
            self._mostrar_funcion_transferencia_teorica(wn, zeta)

            self.v_sim = y_resp
            # Indicar que los datos actuales provienen de la simulación para que la FFT sepa qué analizar
            self.data_origen = "simulacion"
            
            print("Simulación completada y gráfica actualizada")
            
        except Exception as e:
            print(f"❌ Error en simulación: {e}")

    def _mostrar_funcion_transferencia_teorica(self, wn, zeta):
        """Muestra la función de transferencia específica en el frame de ecuaciones."""
        # Limpiar el frame de ecuaciones
        for widget in self.eq_frame.winfo_children():
            widget.destroy()
        
        # Crear nueva ecuación específica
        fig = Figure(figsize=(6, 1.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.axis("off")

        # Función de transferencia específica: G(s) = ωn² / (s² + 2ζωn s + ωn²)
        ecuacion = (
            r"$G(s)=\frac{"
            f"{wn**2:.1f}"
            r"}{s^2 + "
            f"{2*zeta*wn:.1f}"
            r"s + "
            f"{wn**2:.1f}"
            r"}$"
        )

        ax.text(0.5, 0.5, ecuacion, fontsize=18, ha="center", va="center", 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.5))

        canvas = FigureCanvasTkAgg(fig, master=self.eq_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _mostrar_funcion_transferencia_estimada(self, wn, zeta):
        """Muestra la función de transferencia estimada en el frame de ecuaciones."""
        # Limpiar el frame de ecuaciones
        for widget in self.eq_frame.winfo_children():
            widget.destroy()
        
        # Crear nueva ecuación estimada
        fig = Figure(figsize=(6, 1.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.axis("off")

        # Función de transferencia estimada: G_est(s) = ωn² / (s² + 2ζωn s + ωn²)
        ecuacion = (
            r"$G_{est}(s)=\frac{"
            f"{wn**2:.1f}"
            r"}{s^2 + "
            f"{2*zeta*wn:.1f}"
            r"s + "
            f"{wn**2:.1f}"
            r"}$"
        )

        ax.text(0.5, 0.5, ecuacion, fontsize=18, ha="center", va="center", 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.5))

        canvas = FigureCanvasTkAgg(fig, master=self.eq_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def borrar(self):
        self.ax.clear()
        self.canvas.draw()
        self.limpiar_parametros()

        # Restaurar la función de transferencia canónica
        for widget in self.eq_frame.winfo_children():
            widget.destroy()
        self.mostrar_funcion_canonica()

        print("Gráfica y parámetros borrados")

    def mostrar_funcion_canonica(self):
        fig = Figure(figsize=(6, 1.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.axis("off")

        ecuacion = (
            r"$G(s)=\frac{\omega_n^2}"
            r"{s^2 + 2\zeta\omega_n s + \omega_n^2}$"
        )

        ax.text(0.5, 0.5, ecuacion, fontsize=20, ha="center", va="center")

        canvas = FigureCanvasTkAgg(fig, master=self.eq_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def mostrar_fft(self):
        try:
            if self.data_origen is None:
                print(" No hay datos para FFT")
                return

            if self.data_origen == "serial":
                y = self.v_raw
                print(" FFT de datos reales (puerto serial)")
            elif self.data_origen == "simulacion":
                y = self.v_sim
                print(" FFT de señal simulada")
            elif self.data_origen == "archivo":
                y = self.v_load
                print(" FFT de datos cargados desde archivo")
            else:
                print(" Origen de datos desconocido")
                return

            # Preprocesamiento
            y_filt = self.processor.lowpass(y, fc=100)
            y_norm = self.processor.normalize(y_filt)

            # FFT con derivada + suavizado
            freqs, mag, mag_smooth = self.fft_analyzer.compute_fft_escalon(y_norm)

            # Buscar pico en espectro suavizado, ignorando DC
            umbral_dc_hz = 2.0
            idx_inicio = max(np.argmax(freqs > umbral_dc_hz), 1)

            idx_peak = idx_inicio + np.argmax(mag_smooth[idx_inicio:])
            f_peak   = freqs[idx_peak]
            m_peak   = mag[idx_peak]

            print(f"  pico detectado: {f_peak:.2f} Hz  mag={m_peak:.4f}")
            if self.params is not None:
                print(f"  fn estimada   : {self.params['wn']/(2*np.pi):.2f} Hz")

            # Rango del eje X: 5× el pico, mínimo 20 Hz
            x_max = min(max(f_peak * 5, 20), self.fs / 2)

            # Rango del eje Y: máximo real dentro del rango visible
            mask      = (freqs >= freqs[idx_inicio]) & (freqs <= x_max)
            y_max_vis = mag[mask].max() if mask.any() else m_peak

            # Gráfica
            self.ax.clear()
            self.ax.plot(freqs[idx_inicio:], mag[idx_inicio:],
                        linewidth=1.5, alpha=0.6, color='steelblue', label='FFT')
            self.ax.plot(freqs[idx_inicio:], mag_smooth[idx_inicio:],
                        linewidth=2, color='orange', label='Suavizado')
            self.ax.set_title("Espectro de Frecuencia (FFT)")
            self.ax.set_xlabel("Frecuencia (Hz)")
            self.ax.set_ylabel("Magnitud")
            self.ax.grid(True)

            self.ax.set_xlim(0, x_max)
            self.ax.set_ylim(0, y_max_vis * 1.3)

            self.ax.plot(f_peak, m_peak, 'r*', markersize=12,
                        label=f'Pico: {f_peak:.2f} Hz')
            self.ax.axvline(x=f_peak, color='g', linestyle=':', alpha=0.5)
            self.ax.legend(loc='upper right', fontsize=9)

            self.canvas.draw()

        except Exception as e:
            print(f" Error FFT: {e}")