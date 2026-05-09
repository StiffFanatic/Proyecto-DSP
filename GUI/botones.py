import tkinter as tk
from PIL import Image, ImageTk
import os
from GUI.resize import Resizer

class DSPButton:
    def __init__(self, parent, text, color, command=None, img_name=None):
        
        base_dir = os.path.dirname(__file__)

        ancho=20
        alto=5
        # 1. Definimos el tamaño deseado en PÍXELES
       
        ancho_px = ancho*10
        alto_px = alto*10
       
        if img_name:
            # Si hay imagen, la cargamos y redimensionamos
            base_dir = os.path.dirname(__file__)
            img_path = os.path.join(base_dir, "assets", "Imagenes", img_name)
            pil_img = Image.open(img_path).resize((ancho_px, alto_px))
            self.bt_img = ImageTk.PhotoImage(pil_img)
        else:
            # Si no hay imagen, creamos una imagen transparente de 1x1
            # Esto engaña al botón para que use píxeles como unidad de medida
            self.bt_img = tk.PhotoImage(width=1, height=1)
        
        
        # 2. Creamos el botón


        self.button = tk.Button(
            parent,
            text=text,
            image=self.bt_img,
            compound="center", # Fundamental: permite texto sobre la imagen (o la nada)
            #bg=self.bg,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=ancho_px,    # Se lee en píxeles gracias a la imagen
            height=alto_px,    # Se lee en píxeles gracias a la imagen
            command=command
        )       
        if img_name:
            #  se encarga de ajustar la imagen al botón
           self.resize= Resizer(self.button, Image.open(img_path))
           self.bg= self.resize.imgcolor()
           self.button.config(bg=self.bg)
        
        # Evitamos que el recolector de basura borre la imagen
        self.button.image = self.bt_img
        self.button.pack(pady=3)
     
         
    
        
        
        #self.button.pack(fill="x", pady=3, padx=10)
     
class ButtonManager:
    def __init__(self, main_window):
        self.main = main_window
        self.frame = main_window.frame_right
        self._create_buttons()
        

    def _create_buttons(self):
        DSPButton(self.frame, "Conectar", "#2ecc71", self.main.conectar_serial,"cian.jpg")
        DSPButton(self.frame, "Tomar Datos", "#16a085", self.main.capturar_escalon,"azul.jpg")
        DSPButton(self.frame, "Cargar Datos Prueba", "#27ae60", self.main.cargar_datos_prueba,"verde.jpg")
        DSPButton(self.frame, "Borrar", "#e74c3c", self.main.borrar,"rojo.jpg")
        DSPButton(self.frame, "Mostrar Análisis", "#e67e22", self.main.mostrar_analisis,"naranja.jpg")
        DSPButton(self.frame, "FFT", "#f39c12", self.main.mostrar_fft,"mostaza.jpg")
        DSPButton(self.frame, "Simular", "#9b59b6", self.main.simular,"morado.jpg")
        DSPButton(self.frame, "Salir", "#7f8c8d", self.main.root.destroy,"gris.jpg")