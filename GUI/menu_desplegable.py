import tkinter as tk
#from GUI.resize import Resizer
from PIL import Image, ImageTk
import os
"""
MODOS_RLC = {
        "Subamortiguado": (10, 0.1, 100e-6),
        "Criticamente amortiguado": (200, 0.1, 10e-6),
        "Sobreamortiguado": (1000, 0.1, 10e-6),
        }
        """

        
class Menu:
    """Clase para cada opción individual del menú desplegable"""
    def __init__(self, parent, text, width,row, command=None):
        self.parent=parent
        self.text = text
        self.command = command
       
        #self.default_bg = "#4e5254"
        #self.default_bg="#176b6e"
        self.default_bg="#200a8c"
      
        #self.hover_bg = "#afced4"
        #self.hover_bg ="#32e9f0"
        self.hover_bg="#1e78c7"
        self.label = tk.Label(
            parent,
            text=self.text,
            bg=self.default_bg,
            fg="white",
            padx=width,
            pady=8,
            cursor="hand2",
            width=width
        )
        #self.label.pack(side="left", anchor="e")
        self.label.grid(row=row,column=1)
        # Binds para hover y click
        self.label.bind("<Enter>", lambda e: self.label.config(bg=self.hover_bg))
        self.label.bind("<Leave>", lambda e: self.label.config(bg=self.default_bg))
        if self.command:
            self.label.bind("<Button-1>", lambda e: self.command(self.text))

class Menu_desplegable:
    """Clase que gestiona la barra superior y el despliegue del menú"""
    def __init__(self, root,entry_r=0,entry_l=0,entry_c=0):
       
        self.root = root
        self.entry_r = entry_r
        self.entry_l = entry_l
        self.entry_c = entry_c

        self.width = 40
        self.visible = False
        self.MODOS_RLC = {

            "Sub\namortiguado": (10, 0.1, 100e-6),
            "Críticamente\namortiguado": (200, 0.1, 10e-6),
            "Sobre\namortiguado": (1000, 0.1, 10e-6),

        }
        self._setup_ui()
        
    def _setup_ui(self):
        #self.brbg="#8E9194"
        #self.brbg=  "#1d888c"
        self.brbg="#2936ab"
        
        text="Archivo"
        text="Modo de respuesta"
        # 1. Barra superior
        self.barra = tk.Frame(self.root, bg=self.brbg, height=30, width=self.width)
        #self.barra.pack(side="left", anchor="e")
        self.barra.grid(row=0,column=1,sticky="ne")
        
        # 2. Botón "Archivo" que dispara el menú
        self.btn_archivo = tk.Label(
            self.barra,
            text=text,
            bg=self.brbg,
            fg="white",
             relief="raised",
            padx=self.width,
            pady=5,
            cursor="hand2",
            width=self.width
        )
        #self.btn_archivo.pack(side="top")
        self.btn_archivo.grid(row=0, column=0)
        #self.btn_archivo.grid(row=0,column=1)
        self.btn_archivo.bind("<Button-1>", self.toggle_menu)
        
        # 3. Contenedor del menú (inicialmente oculto)
        self.menu_frame = tk.Frame(
            self.barra,
            bg=self.brbg,
            bd=1,
            relief="solid"
        )
        
        # 4. Crear las opciones
        self._create_menu_items()

    def _create_menu_items(self):
        opciones=["Sobre\namortiguado","Sub\namortiguado","Críticamente\namortiguado"]
        
        self.wdth=self.width
        for i,opcion in enumerate(opciones):
            
            Menu(
                self.menu_frame, 
                opcion, 
                self.width, 
                row=i, # Pasamos el índice como fila
                command=self.accion_menu
            )
            self.wdth+=self.width
           
    def accion_menu(self, nombre_opcion):
    
        if nombre_opcion in self.MODOS_RLC:
             R, L, C = self.MODOS_RLC[nombre_opcion]
             self.entry_r.delete(0, tk.END)
             self.entry_r.insert(0, str(R))
           # if hasattr(self.entry_l, 'delete'):
             self.entry_l.delete(0, tk.END)
             self.entry_l.insert(0, str(L))
            #if hasattr(self.entry_c, 'delete'):
             self.entry_c.delete(0, tk.END)
             self.entry_c.insert(0, str(C))

        self.toggle_menu(None) # Opcional: cerrar al hacer click

    def toggle_menu(self, event):
        if self.visible:
            #self.menu_frame.pack_forget()
            self.menu_frame.grid_forget()
        else:
           # self.menu_frame.pack(side="top", anchor="e")
           self.menu_frame.grid(row=1,column=0,sticky="ne")
        self.visible = not self.visible
