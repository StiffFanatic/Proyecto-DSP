import tkinter as tk

class DSPButton:
    def __init__(self, parent, text, color, command=None):
        self.button = tk.Button(
            parent,
            text=text,
            bg=color,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="raised",
            bd=2,
            height=2,
            command=command
        )
        self.button.pack(fill="x", pady=8)


class ButtonManager:
    def __init__(self, main_window):
        self.main = main_window
        self.frame = main_window.frame_right
        self._create_buttons()

    def _create_buttons(self):
        DSPButton(self.frame, "Conectar", "#2ecc71", self.main.conectar_serial)
        DSPButton(self.frame, "Tomar Datos", "#16a085", self.main.capturar_escalon)
        DSPButton(self.frame, "Cargar Datos Prueba", "#27ae60", self.main.cargar_datos_prueba)
        DSPButton(self.frame, "Borrar", "#e74c3c", self.main.borrar)
        DSPButton(self.frame, "Mostrar Análisis", "#e67e22", self.main.mostrar_analisis)
        DSPButton(self.frame, "FFT", "#f39c12", self.main.mostrar_fft)
        DSPButton(self.frame, "Simular", "#9b59b6", self.main.simular)
        DSPButton(self.frame, "Salir", "#7f8c8d", self.main.root.destroy)