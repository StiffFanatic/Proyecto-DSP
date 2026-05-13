import tkinter as tk

class Menu:
    """Clase para cada opción individual del menú desplegable"""
    def __init__(self, parent, text, width,row, command=None):
        self.parent=parent
        self.i=1
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
    def __init__(self, root):
        self.root = root
        self.width = 40
        self.visible = False
        
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
        opciones=["sobre\namortiguado","sub\namortiguado","críticamente\namortiguado"]
        self.i=1
        for i, opcion in enumerate(opciones):
            Menu(
                self.menu_frame, 
                opcion, 
                self.width, 
                row=i, # Pasamos el índice como fila
                command=self.accion_menu
            )
    def accion_menu(self, nombre_opcion):
        print(f"Acción ejecutada: {nombre_opcion}")
        self.toggle_menu(None) # Opcional: cerrar al hacer click

    def toggle_menu(self, event):
        if self.visible:
            #self.menu_frame.pack_forget()
            self.menu_frame.grid_forget()
        else:
           # self.menu_frame.pack(side="top", anchor="e")
           self.menu_frame.grid(row=1,column=0,sticky="ne")
        self.visible = not self.visible

# --- Ejemplo de uso ---
if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("Menu Clase")
    ventana.config(bg="#dde3e8")
    ventana.geometry("400x300")
    
    # Instanciamos el manager del menú
    menu_app = Menu_desplegable(ventana)
    
    ventana.mainloop()